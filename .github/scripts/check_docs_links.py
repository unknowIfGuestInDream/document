#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs"
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)


@dataclass
class Problem:
    file: Path
    line: int
    link: str
    problem: str
    suggestion: str


def iter_candidate_files(paths: Sequence[str]) -> Iterator[Path]:
    if not paths:
        yield from sorted(DOCS_ROOT.rglob("*.md"))
        return

    for raw_path in paths:
        path = (REPO_ROOT / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path).resolve()
        if not path.exists():
            continue
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*.md") if p.is_file())
        elif path.suffix.lower() == ".md":
            yield path


def strip_code_fences(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    inside_fence = False
    fence_marker = ""
    for line_number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not inside_fence:
                inside_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                inside_fence = False
                fence_marker = ""
            continue
        if not inside_fence:
            yield line_number, line


def normalize_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if not destination:
        return destination
    if destination.startswith("<"):
        destination = destination[1:].split(">", 1)[0]
    else:
        destination = destination.split(maxsplit=1)[0]
    return destination


def is_external_link(destination: str) -> bool:
    lowered = destination.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "javascript:"))


def resolve_target(current_file: Path, destination: str) -> list[Path]:
    path_part = destination.split("#", 1)[0].split("?", 1)[0]
    if destination == "/":
        return [DOCS_ROOT / "README.md"]
    if path_part.startswith("/"):
        relative = path_part.lstrip("/")
        bases = [DOCS_ROOT / relative]
    else:
        bases = [
            (current_file.parent / path_part).resolve(),
            (DOCS_ROOT / path_part).resolve(),
        ]

    candidates: list[Path] = []
    for base in bases:
        candidates.append(base)
        if base.suffix:
            continue
        candidates.extend([
            Path(str(base) + ".md"),
            base / "README.md",
            base / "index.md",
        ])
    return candidates


def find_problems(markdown_file: Path) -> list[Problem]:
    problems: list[Problem] = []
    content = markdown_file.read_text(encoding="utf-8")

    for line_number, line in strip_code_fences(content.splitlines()):
        destinations = [match.group(1) for match in MARKDOWN_LINK_RE.finditer(line)]
        destinations.extend(match.group(1) for match in HTML_SRC_RE.finditer(line))
        for raw_destination in destinations:
            destination = normalize_destination(raw_destination)
            if not destination:
                problems.append(Problem(markdown_file, line_number, raw_destination, "Empty link target.", "Provide a valid local or external target."))
                continue
            if destination.startswith("#") or is_external_link(destination):
                continue

            candidates = resolve_target(markdown_file, destination)
            if any(candidate.is_file() for candidate in candidates):
                continue

            preferred = candidates[1] if len(candidates) > 1 else candidates[0]
            try:
                suggestion = preferred.relative_to(REPO_ROOT)
            except ValueError:
                suggestion = preferred
            problems.append(
                Problem(
                    markdown_file,
                    line_number,
                    destination,
                    "Local Docsify or Markdown target does not exist.",
                    f"Check the relative path or create `{suggestion}`.",
                )
            )

    return problems


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="Check local Docsify/Markdown links in repository documentation files.")
    parser.add_argument("paths", nargs="*", help="Markdown files or directories to check. Defaults to docs/**/*.md.")
    args = parser.parse_args(argv)

    files = list(dict.fromkeys(iter_candidate_files(args.paths)))
    if not files:
        print("No Markdown files to check.")
        return 0

    all_problems: list[Problem] = []
    for file in files:
        all_problems.extend(find_problems(file))

    if not all_problems:
        print(f"Checked {len(files)} Markdown file(s); no local link problems found.")
        return 0

    for problem in all_problems:
        try:
            display_path = problem.file.relative_to(REPO_ROOT)
        except ValueError:
            display_path = problem.file
        print(f"File: {display_path}")
        print(f"Line: {problem.line}")
        print(f"Link: {problem.link}")
        print(f"Problem: {problem.problem}")
        print(f"Suggested fix: {problem.suggestion}")
        print()

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
