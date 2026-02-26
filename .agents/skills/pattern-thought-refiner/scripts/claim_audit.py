#!/usr/bin/env python3
"""Flag strong claims that likely require evidence."""

from __future__ import annotations

import re
import sys
from pathlib import Path

TRIGGERS = [
    "always",
    "never",
    "guarantee",
    "proven",
    "best",
    "state of the art",
    "100%",
    "eliminates",
    "zero",
    "dramatically",
    "significantly",
]


def split_sentences(text: str) -> list[str]:
    raw = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in raw if part.strip()]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: claim_audit.py <markdown-file>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    flagged = []

    for sentence in split_sentences(text):
        lower = sentence.lower()
        hits = [token for token in TRIGGERS if token in lower]
        if hits:
            flagged.append((sentence, hits))

    if not flagged:
        print("PASS: No obvious high-certainty claim triggers found.")
        return 0

    print("REVIEW: Claims that may require explicit evidence or softening:")
    for idx, (sentence, hits) in enumerate(flagged, start=1):
        tokens = ", ".join(hits)
        print(f"{idx}. [{tokens}] {sentence}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
