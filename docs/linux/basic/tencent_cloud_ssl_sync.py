#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

CERT_DIR = Path("/etc/nginx/cert")
STATE_DIR = Path("/var/lib/tencent-ssl-sync")

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
    "blog.tlcsdm.com": "tlcsdm.com",
    "www.tlcsdm.com": "tlcsdm.com",
}


def run_tccli(service: str, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cmd = ["tccli", service, action, "--output", "json"]
    if params:
        for key, value in params.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            cmd.extend([f"--{key}", str(value)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"tccli 调用失败: {' '.join(cmd)}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"tccli 输出不是有效 JSON: {result.stdout}") from exc


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def extract_domains_from_cert(cert: Dict[str, Any]) -> List[str]:
    domains: List[str] = []
    primary = cert.get("Domain")
    if isinstance(primary, str) and primary:
        domains.append(primary.strip())

    san = cert.get("SubjectAltName")
    if isinstance(san, list):
        domains.extend([item.strip() for item in san if isinstance(item, str) and item.strip()])
    elif isinstance(san, str) and san.strip():
        domains.extend([part.strip() for part in san.split(",") if part.strip()])

    return list(dict.fromkeys(domains))


def cert_matches_domain(cert: Dict[str, Any], domain: str) -> bool:
    for cert_domain in extract_domains_from_cert(cert):
        if cert_domain == domain:
            return True
        if cert_domain.startswith("*.") and domain.endswith(cert_domain[1:]):
            return True
    return False


def get_latest_certificate_for_domain(domain: str) -> Dict[str, Any]:
    search_key = CERT_QUERY_DOMAIN_OVERRIDES.get(domain, domain)
    resp = run_tccli(
        "ssl",
        "DescribeCertificates",
        {
            "SearchKey": search_key,
            "Limit": 100,
            "Offset": 0,
        },
    )

    certificates = resp.get("Response", {}).get("Certificates", [])
    if not certificates:
        raise RuntimeError(f"未查询到证书: {domain} (SearchKey={search_key})")

    matched = [cert for cert in certificates if cert_matches_domain(cert, domain) or cert_matches_domain(cert, search_key)]
    if not matched:
        matched = certificates

    def cert_sort_key(cert: Dict[str, Any]) -> dt.datetime:
        parsed_dates: List[dt.datetime] = []
        for field in ("CertBeginTime", "CertEndTime"):
            value = cert.get(field)
            if isinstance(value, str) and value:
                try:
                    parsed_dates.append(parse_time(value))
                except ValueError:
                    continue
        return max(parsed_dates) if parsed_dates else dt.datetime.min

    return max(matched, key=cert_sort_key)


def download_certificate(certificate_id: str) -> Tuple[str, str]:
    resp = run_tccli("ssl", "DownloadCertificate", {"CertificateId": certificate_id})
    payload = resp.get("Response", {})
    cert_pem = payload.get("Certificate")
    key_pem = payload.get("PrivateKey")
    if not cert_pem or not key_pem:
        raise RuntimeError(f"下载证书失败或证书不含私钥: {certificate_id}")
    return cert_pem, key_pem


def write_file_atomic(path: Path, content: str, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent)) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fchmod(tmp.fileno(), mode)
        temp_path = Path(tmp.name)
    os.replace(temp_path, path)


def backup_file(path: Path) -> None:
    if not path.exists():
        return
    backup_root = STATE_DIR / "backup"
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%SZ")
    backup_path = backup_root / f"{path.name}.{timestamp}.bak"
    shutil.copy2(path, backup_path)


def update_nginx_cert_files(domain: str, cert_pem: str, key_pem: str, dry_run: bool = False) -> bool:
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

    backup_file(cert_file)
    backup_file(key_file)
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


def reload_nginx(dry_run: bool = False) -> None:
    print("[NGINX] 重新加载配置")
    if dry_run:
        return
    subprocess.run(["nginx", "-t"], check=True)
    subprocess.run(["systemctl", "reload", "nginx"], check=True)


def ensure_dependencies() -> None:
    if shutil.which("tccli") is None:
        raise RuntimeError("未找到 tccli，请先安装并配置腾讯云 CLI 凭据")


def run(dry_run: bool = False, skip_nginx_reload: bool = False) -> int:
    ensure_dependencies()

    cert_cache: Dict[str, Tuple[str, str]] = {}
    certificate_selection: Dict[str, Dict[str, Any]] = {}

    # 保留配置顺序并去重，确保日志输出顺序稳定
    all_domains = list(dict.fromkeys(NGINX_CERT_DOMAINS + CDN_DOMAINS))

    for domain in all_domains:
        latest_cert = get_latest_certificate_for_domain(domain)
        certificate_selection[domain] = latest_cert
        cert_id = latest_cert.get("CertificateId", "")
        end_time = latest_cert.get("CertEndTime", "unknown")
        print(f"[SSL] {domain}: 选中证书 {cert_id} (过期时间: {end_time})")

    nginx_changed = False
    for domain in NGINX_CERT_DOMAINS:
        cert_id = get_certificate_id_for_domain(certificate_selection, domain)
        if cert_id not in cert_cache:
            cert_cache[cert_id] = download_certificate(cert_id)
        cert_pem, key_pem = cert_cache[cert_id]
        changed = update_nginx_cert_files(domain, cert_pem, key_pem, dry_run=dry_run)
        nginx_changed = nginx_changed or changed

    for domain in CDN_DOMAINS:
        cert_id = get_certificate_id_for_domain(certificate_selection, domain)
        update_cdn_domain_cert(domain, cert_id, dry_run=dry_run)

    if nginx_changed and not skip_nginx_reload:
        reload_nginx(dry_run=dry_run)

    print("完成：证书检查与同步流程结束")
    return 0


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="腾讯云 SSL 证书同步脚本（Nginx + CDN）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将执行的操作，不写入文件、不调用更新 API")
    parser.add_argument("--skip-nginx-reload", action="store_true", help="更新证书后不执行 nginx reload")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    try:
        return run(dry_run=args.dry_run, skip_nginx_reload=args.skip_nginx_reload)
    except Exception as exc:
        print(f"执行失败: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
