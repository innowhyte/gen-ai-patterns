#!/usr/bin/env python3
"""Validate section coverage against the repository pattern template."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = ["problem", "condition", "solution", "example"]
RECOMMENDED = ["tradeoffs", "failure modes"]
OPTIONAL = ["references"]


def normalize_heading(text: str) -> str:
    cleaned = re.sub(r"\(.*?\)", "", text)
    return cleaned.strip().lower()


def collect_headings(content: str) -> set[str]:
    headings = set()
    for line in content.splitlines():
        if line.startswith("## "):
            headings.add(normalize_heading(line[3:]))
    return headings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_pattern_sections.py <markdown-file>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    headings = collect_headings(text)

    missing_required = [name for name in REQUIRED if name not in headings]
    missing_recommended = [name for name in RECOMMENDED if name not in headings]
    missing_optional = [name for name in OPTIONAL if name not in headings]

    if missing_required:
        print("FAIL: Missing required sections:")
        for item in missing_required:
            print(f"- {item.title()}")
    else:
        print("PASS: All required sections are present.")

    if missing_recommended:
        print("INFO: Missing recommended sections:")
        for item in missing_recommended:
            print(f"- {item.title()}")

    if missing_optional:
        print("INFO: Missing optional sections:")
        for item in missing_optional:
            print(f"- {item.title()}")

    # Also flag empty required sections.
    for name in REQUIRED:
        section_re = re.compile(
            rf"^##\s+{re.escape(name)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
            flags=re.IGNORECASE | re.MULTILINE,
        )
        match = section_re.search(text)
        if not match:
            continue
        body = match.group(1).strip()
        if not body:
            print(f"FAIL: Section '{name.title()}' is empty.")
            if name in missing_required:
                continue
            return 1

    return 1 if missing_required else 0


if __name__ == "__main__":
    raise SystemExit(main())
