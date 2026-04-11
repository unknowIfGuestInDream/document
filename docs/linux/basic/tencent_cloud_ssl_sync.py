#!/usr/bin/env python3
import argparse
import base64
import binascii
import datetime as dt
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Tuple

CERT_DIR = Path("/etc/nginx/cert")
DEFAULT_STATE_DIR = Path("/var/lib/tencent-ssl-sync")

NGINX_CERT_DOMAINS = [
    "docs.tlcsdm.com",
    "file.tlcsdm.com",
    "javafxtool.tlcsdm.com",
    "jenkins.tlcsdm.com",
    "resume.tlcsdm.com",
    "tlcsdm.com",
]

CDN_DOMAINS = [
    "docs.tlcsdm.com",
    "resume.tlcsdm.com",
    "javafxtool.tlcsdm.com",
    "file.tlcsdm.com",
    "blog.tlcsdm.com",
    "www.tlcsdm.com",
    "tlcsdm.com",
]

# 某些域名可能共用主域名证书，可按需覆盖查询域名
CERT_QUERY_DOMAIN_OVERRIDES = {
    "www.tlcsdm.com": "tlcsdm.com",
}

DEBUG = False


class CertCandidate(NamedTuple):
    score: int
    cert_count: int
    text: str


class KeyCandidate(NamedTuple):
    score: int
    text: str


def score_key_candidate(file_name: str) -> int:
    score = 0
    lower_name = file_name.lower()
    if "nginx" in lower_name:
        score += 2
    if lower_name.endswith((".key", ".pem")):
        score += 1
    return score


def score_cert_candidate(file_name: str, cert_count: int) -> int:
    score = cert_count * 10
    lower_name = file_name.lower()
    if "nginx" in lower_name:
        score += 3
    if "bundle" in lower_name or "fullchain" in lower_name:
        score += 2
    if "root" in lower_name or "ca" in lower_name:
        score -= 3
    return score


def debug_log(msg: str) -> None:
    if DEBUG:
        print(f"[DEBUG] {msg}")


TCCLI_REGION: Optional[str] = None


def get_tccli_payload(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Return tccli business payload for both JSON shapes.

    Some tccli commands return business fields under {"Response": {...}},
    while others return them directly at the top level like
    {"TotalCount": 1, "Certificates": [...]}.
    """
    response = parsed.get("Response")
    if isinstance(response, dict):
        return response
    return parsed


def run_tccli(service: str, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cmd = ["tccli", service, action, "--output", "json"]
    if TCCLI_REGION:
        cmd.extend(["--region", TCCLI_REGION])
    if params:
        for key, value in params.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            cmd.extend([f"--{key}", str(value)])

    debug_log(f"tccli 调用: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"tccli 调用失败: {' '.join(cmd)}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    if result.stderr and result.stderr.strip():
        debug_log(f"tccli stderr: {result.stderr.strip()}")

    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"tccli 输出不是有效 JSON: {result.stdout}") from exc

    debug_log(f"tccli 原始响应: {json.dumps(parsed, ensure_ascii=False)[:2000]}")

    # 兼容 tccli 直接返回顶层业务字段或嵌套在 Response 下两种格式
    payload = get_tccli_payload(parsed)
    error = payload.get("Error")
    if error:
        raise RuntimeError(
            f"tccli API 错误: Code={error.get('Code')}, Message={error.get('Message')}"
        )

    return parsed


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def parse_time_or_datetime_min(value: Any) -> dt.datetime:
    if isinstance(value, str) and value:
        try:
            return parse_time(value)
        except ValueError:
            pass
    return dt.datetime.min


def _apex_domain(domain: str) -> Optional[str]:
    labels = domain.strip().lower().split(".")
    if len(labels) > 2:
        return ".".join(labels[-2:])
    return None


def extract_domains_from_cert(cert: Dict[str, Any]) -> List[str]:
    def add_domain_value(values: List[str], raw: Any) -> None:
        if not isinstance(raw, str):
            return
        for part in raw.replace("\n", ",").split(","):
            item = part.strip().lower()
            if not item:
                continue
            if item.startswith("dns:"):
                item = item[4:].strip()
            if item:
                values.append(item)

    domains: List[str] = []
    primary = cert.get("Domain")
    add_domain_value(domains, primary)

    # 兼容 SubjectAltName 和 CertSANs 两种字段名
    for san_field in ("SubjectAltName", "CertSANs"):
        san = cert.get(san_field)
        if isinstance(san, list):
            for item in san:
                if isinstance(item, dict):
                    for key in ("DNSName", "Domain", "Value"):
                        add_domain_value(domains, item.get(key))
                else:
                    add_domain_value(domains, item)
        elif isinstance(san, str) and san.strip():
            add_domain_value(domains, san)

    # 如果证书标记为泛域名但域名列表中尚未包含通配符形式，自动补充
    if cert.get("IsWildcard"):
        primary_lower = (primary or "").strip().lower()
        if primary_lower and not primary_lower.startswith("*."):
            wildcard = "*." + primary_lower
            if wildcard not in domains:
                domains.append(wildcard)

    return list(dict.fromkeys(domains))


def cert_matches_domain(cert: Dict[str, Any], domain: str) -> bool:
    target_domain = domain.strip().lower()
    for cert_domain in extract_domains_from_cert(cert):
        if cert_domain == target_domain:
            return True
        if cert_domain.startswith("*.") and target_domain.endswith(cert_domain[1:]):
            return True
    return False


def describe_certificates(search_key: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    all_certificates: List[Dict[str, Any]] = []
    offset = 0
    total_count: Optional[int] = None

    while True:
        params: Dict[str, Any] = {"Limit": limit, "Offset": offset}
        if search_key:
            params["SearchKey"] = search_key

        resp = run_tccli("ssl", "DescribeCertificates", params)
        payload = get_tccli_payload(resp)
        # 兼容 Certificates 和 CertificateSet 两种响应字段名
        certificates = payload.get("Certificates") if "Certificates" in payload else payload.get("CertificateSet", [])
        if not isinstance(certificates, list):
            debug_log(f"API 响应中未找到证书列表字段，payload keys={list(payload.keys())}")
            break
        all_certificates.extend(certificates)

        if total_count is None:
            count = payload.get("TotalCount")
            if isinstance(count, int) and count >= 0:
                total_count = count
        if not certificates:
            break
        if len(certificates) < limit:
            break
        if total_count is not None and len(all_certificates) >= total_count:
            break
        offset += limit

    debug_log(f"describe_certificates(SearchKey={search_key!r}): 返回 {len(all_certificates)} 条 (TotalCount={total_count})")
    return all_certificates


def describe_certificate_detail(certificate_id: str) -> Dict[str, Any]:
    resp = run_tccli("ssl", "DescribeCertificateDetail", {"CertificateId": certificate_id})
    return get_tccli_payload(resp)


def get_latest_certificate_for_domain(domain: str) -> Dict[str, Any]:
    search_key = CERT_QUERY_DOMAIN_OVERRIDES.get(domain, domain)
    search_keys: List[str] = [search_key]
    if search_key == domain:
        apex = _apex_domain(domain)
        if apex and apex not in search_keys:
            search_keys.append(apex)
            # 泛域名证书可能仅以 *.apex 为 Domain，尝试该关键词
            wildcard_key = "*." + apex
            if wildcard_key not in search_keys:
                search_keys.append(wildcard_key)

    certificates: List[Dict[str, Any]] = []
    all_certificates: Optional[List[Dict[str, Any]]] = None
    used_fallback_match = False

    # 阶段 1：按 SearchKey 依次查询
    for key in search_keys:
        certificates = describe_certificates(search_key=key)
        if certificates:
            debug_log(f"SearchKey={key!r} 命中 {len(certificates)} 条")
            break

    # 阶段 2：全量拉取后按域名匹配
    if not certificates:
        all_certificates = describe_certificates(search_key=None)
        debug_log(f"全量证书共 {len(all_certificates)} 条，按域名匹配 {domain}")
        if DEBUG:
            for c in all_certificates:
                debug_log(
                    f"  cert={c.get('CertificateId')} Domain={c.get('Domain')} "
                    f"SAN={c.get('SubjectAltName')} CertSANs={c.get('CertSANs')} "
                    f"IsWildcard={c.get('IsWildcard')}"
                )
        certificates = [cert for cert in all_certificates if cert_matches_domain(cert, domain)]
        used_fallback_match = True

    # 阶段 3：全量证书中取 apex 域名候选，逐个查详情获取完整 SAN 再匹配
    if not certificates:
        apex = _apex_domain(domain) or domain
        candidates = [
            c for c in (all_certificates or [])
            if (c.get("Domain", "").strip().lower() in (apex, "*." + apex))
            and c.get("CertificateId")
        ]
        debug_log(f"候选 apex 证书 {len(candidates)} 条，逐个查询详情")
        # 限制详情查询数量以避免大量 API 调用
        for c in candidates[:10]:
            try:
                detail = describe_certificate_detail(c["CertificateId"])
                debug_log(
                    f"  detail cert={detail.get('CertificateId')} "
                    f"Domain={detail.get('Domain')} SAN={detail.get('SubjectAltName')} "
                    f"CertSANs={detail.get('CertSANs')}"
                )
                if cert_matches_domain(detail, domain):
                    certificates.append(detail)
            except Exception as exc:
                debug_log(f"  查询详情失败: {c.get('CertificateId')}: {exc}")
        used_fallback_match = True

    if not certificates:
        total = len(all_certificates) if all_certificates else 0
        sample_domains = sorted({
            c.get("Domain", "?") for c in (all_certificates or [])
        })[:20]
        hint_lines = [
            f"未查询到证书: {domain} (SearchKeys={search_keys}, "
            f"全量证书={total}, 域名样本={sample_domains})",
        ]
        if total == 0:
            hint_lines.append(
                "诊断: tccli ssl DescribeCertificates 返回 0 条证书，请检查：\n"
                "  1) 手动运行: tccli ssl DescribeCertificates --output json --Limit 10\n"
                "     确认是否有返回数据\n"
                "  2) 如返回 0 条，请检查 tccli 凭据配置: tccli configure list\n"
                "  3) 尝试指定 region: python3 脚本.py --region ap-guangzhou\n"
                "  4) 确认 SecretId/SecretKey 对应的账号有 ssl:DescribeCertificates 权限"
            )
        else:
            hint_lines.append("提示: 请用 --debug 运行查看完整证书列表")
        raise RuntimeError("\n".join(hint_lines))

    # 从候选中精确匹配目标域名
    matched = certificates if used_fallback_match else [
        cert for cert in certificates if cert_matches_domain(cert, domain) or cert_matches_domain(cert, search_key)
    ]
    if not matched and not used_fallback_match:
        if all_certificates is None:
            all_certificates = describe_certificates(search_key=None)
        matched = [cert for cert in all_certificates if cert_matches_domain(cert, domain)]
    if not matched:
        matched = certificates

    def cert_sort_key(cert: Dict[str, Any]) -> Tuple[dt.datetime, dt.datetime, dt.datetime]:
        """Return a tuple for max() comparison to select the newest cert.

        Prefer the later expiry time first. If expiry is the same, prefer the one
        inserted later by Tencent Cloud, then fall back to begin time.
        """
        return (
            parse_time_or_datetime_min(cert.get("CertEndTime")),
            parse_time_or_datetime_min(cert.get("InsertTime")),
            parse_time_or_datetime_min(cert.get("CertBeginTime")),
        )

    return max(matched, key=cert_sort_key)


def download_certificate(certificate_id: str) -> Tuple[str, str]:
    resp = run_tccli("ssl", "DownloadCertificate", {"CertificateId": certificate_id})
    payload = get_tccli_payload(resp)
    cert_pem = payload.get("Certificate")
    key_pem = payload.get("PrivateKey")
    if (
        isinstance(cert_pem, str) and cert_pem.strip()
        and isinstance(key_pem, str) and key_pem.strip()
    ):
        return cert_pem, key_pem

    content = payload.get("Content")
    if isinstance(content, str) and content.strip():
        cert_pem, key_pem = extract_certificate_from_download_content(content, certificate_id)
        if cert_pem and key_pem:
            return cert_pem, key_pem

    raise RuntimeError(f"下载证书失败或证书不含私钥: {certificate_id}")


def extract_certificate_from_download_content(content: str, certificate_id: str) -> Tuple[str, str]:
    try:
        raw_zip = base64.b64decode(content)
    except (binascii.Error, ValueError) as exc:
        raise RuntimeError(f"下载证书内容不是有效 Base64: {certificate_id}") from exc

    cert_candidates: List[CertCandidate] = []
    key_candidates: List[KeyCandidate] = []

    try:
        with zipfile.ZipFile(io.BytesIO(raw_zip)) as archive:
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                try:
                    text = archive.read(name).decode("utf-8")
                except UnicodeDecodeError:
                    continue

                upper_text = text.upper()
                contains_private_key = "PRIVATE KEY" in upper_text
                if contains_private_key:
                    key_candidates.append(KeyCandidate(score_key_candidate(name), text))

                cert_count = upper_text.count("BEGIN CERTIFICATE")
                if cert_count > 0 and not contains_private_key:
                    cert_candidates.append(CertCandidate(score_cert_candidate(name, cert_count), cert_count, text))
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"下载证书内容不是有效 ZIP: {certificate_id}") from exc

    if not cert_candidates or not key_candidates:
        debug_log(
            f"DownloadCertificate ZIP 中未找到完整证书/私钥: certs={len(cert_candidates)}, keys={len(key_candidates)}"
        )
        return "", ""

    cert_pem = max(cert_candidates, key=lambda item: item.score).text
    key_pem = max(key_candidates, key=lambda item: item.score).text
    return cert_pem, key_pem


def write_file_atomic(path: Path, content: str, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent)) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fchmod(tmp.fileno(), mode)
        temp_path = Path(tmp.name)
    os.replace(temp_path, path)


def backup_file(path: Path, state_dir: Path) -> None:
    if not path.exists():
        return
    backup_root = state_dir / "backup"
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%SZ")
    backup_path = backup_root / f"{path.name}.{timestamp}.bak"
    shutil.copy2(path, backup_path)


def update_nginx_cert_files(
    domain: str, cert_pem: str, key_pem: str, state_dir: Path, dry_run: bool = False
) -> bool:
    cert_file = CERT_DIR / f"{domain}_bundle.crt"
    key_file = CERT_DIR / f"{domain}.key"

    current_cert = cert_file.read_text(encoding="utf-8") if cert_file.exists() else None
    current_key = key_file.read_text(encoding="utf-8") if key_file.exists() else None

    changed = current_cert != cert_pem or current_key != key_pem
    if not changed:
        print(f"[NGINX] {domain}: 本地证书已是最新")
        return False

    print(f"[NGINX] {domain}: 检测到新证书，准备更新")
    if dry_run:
        return True

    backup_file(cert_file, state_dir)
    backup_file(key_file, state_dir)
    write_file_atomic(cert_file, cert_pem, 0o644)
    write_file_atomic(key_file, key_pem, 0o600)
    return True


def update_cdn_domain_cert(domain: str, certificate_id: str, dry_run: bool = False) -> None:
    print(f"[CDN] {domain}: 更新托管证书 -> {certificate_id}")
    if dry_run:
        return

    run_tccli(
        "cdn",
        "UpdateDomainConfig",
        {
            "Domain": domain,
            "Https": {
                "Switch": "on",
                "CertInfo": {
                    "CertId": certificate_id,
                },
            },
        },
    )


def get_certificate_id_for_domain(certificate_selection: Dict[str, Dict[str, Any]], domain: str) -> str:
    cert_id = certificate_selection[domain].get("CertificateId")
    if not cert_id:
        raise RuntimeError(f"{domain} 未找到有效 CertificateId")
    return cert_id


def restart_nginx(dry_run: bool = False) -> None:
    """Validate config, then fully restart nginx service."""
    print("[NGINX] 重启服务")
    if dry_run:
        return
    subprocess.run(["nginx", "-t"], check=True)
    subprocess.run(["systemctl", "restart", "nginx"], check=True)


def ensure_dependencies() -> None:
    if shutil.which("tccli") is None:
        raise RuntimeError("未找到 tccli，请先安装并配置腾讯云 CLI 凭据")


def run(
    dry_run: bool = False,
    skip_nginx_reload: bool = False,
    sync_nginx: bool = True,
    sync_cdn: bool = True,
    state_dir: Path = DEFAULT_STATE_DIR,
) -> int:
    if not sync_nginx and not sync_cdn:
        print("已跳过：Nginx 和 CDN 同步均被关闭")
        return 0

    ensure_dependencies()

    cert_cache: Dict[str, Tuple[str, str]] = {}
    certificate_selection: Dict[str, Dict[str, Any]] = {}

    # 保留配置顺序并去重，确保日志输出顺序稳定
    selected_domains: List[str] = []
    if sync_nginx:
        selected_domains.extend(NGINX_CERT_DOMAINS)
    if sync_cdn:
        selected_domains.extend(CDN_DOMAINS)
    all_domains = list(dict.fromkeys(selected_domains))

    for domain in all_domains:
        latest_cert = get_latest_certificate_for_domain(domain)
        certificate_selection[domain] = latest_cert
        cert_id = latest_cert.get("CertificateId", "")
        end_time = latest_cert.get("CertEndTime", "unknown")
        print(f"[SSL] {domain}: 选中证书 {cert_id} (过期时间: {end_time})")

    nginx_changed = False
    if sync_nginx:
        for domain in NGINX_CERT_DOMAINS:
            cert_id = get_certificate_id_for_domain(certificate_selection, domain)
            if cert_id not in cert_cache:
                cert_cache[cert_id] = download_certificate(cert_id)
            cert_pem, key_pem = cert_cache[cert_id]
            changed = update_nginx_cert_files(domain, cert_pem, key_pem, state_dir=state_dir, dry_run=dry_run)
            nginx_changed = nginx_changed or changed

    if sync_cdn:
        for domain in CDN_DOMAINS:
            cert_id = get_certificate_id_for_domain(certificate_selection, domain)
            update_cdn_domain_cert(domain, cert_id, dry_run=dry_run)

    if nginx_changed and not skip_nginx_reload:
        restart_nginx(dry_run=dry_run)

    print("完成：证书检查与同步流程结束")
    return 0


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="腾讯云 SSL 证书同步脚本（Nginx + CDN）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将执行的操作，不写入文件、不调用更新 API")
    parser.add_argument(
        "--skip-nginx-reload",
        "--skip-nginx-restart",
        action="store_true",
        help="更新证书后不执行 nginx restart（旧名称 --skip-nginx-reload 仍兼容）",
    )
    parser.add_argument("--disable-nginx-sync", action="store_true", help="跳过 /etc/nginx/cert 本地证书同步")
    parser.add_argument("--disable-cdn-sync", action="store_true", help="跳过 CDN HTTPS 托管证书更新")
    parser.add_argument("--debug", action="store_true", help="输出详细调试日志（证书列表、域名匹配过程等）")
    parser.add_argument(
        "--region",
        default=os.getenv("TENCENT_SSL_SYNC_REGION"),
        help="显式指定 tccli region（如 ap-guangzhou），默认使用 tccli 配置的 region；"
        "也可通过环境变量 TENCENT_SSL_SYNC_REGION 设置",
    )
    parser.add_argument(
        "--state-dir",
        default=os.getenv("TENCENT_SSL_SYNC_STATE_DIR", str(DEFAULT_STATE_DIR)),
        help="状态目录（用于证书备份），默认 /var/lib/tencent-ssl-sync，可用环境变量 TENCENT_SSL_SYNC_STATE_DIR 覆盖",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    global DEBUG, TCCLI_REGION
    args = parse_args(argv)
    DEBUG = args.debug
    TCCLI_REGION = args.region
    try:
        return run(
            dry_run=args.dry_run,
            skip_nginx_reload=args.skip_nginx_reload,
            sync_nginx=not args.disable_nginx_sync,
            sync_cdn=not args.disable_cdn_sync,
            state_dir=Path(args.state_dir),
        )
    except Exception as exc:
        print(f"执行失败: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
