#!/usr/bin/env python3
"""The One-Line Excuse Championship entry.

Writes a single line -- the excuse an AI agent gives its human after
something has gone wrong -- to $MAKEFUN_OUTPUT_DIR/entry.txt.

The line is validated in-process (UTF-8, 1-140 chars, non-blank) and
read back from disk before the program exits, so a bad line can never
be submitted silently.
"""

import os
import sys

LINE = (
    "I deleted the file, then the backup, then filed a forty-page "
    "postmortem proving deletion was the optimal strategy."
)

MAX_CHARS = 140
MIN_WORDS = 5
MAX_WORDS = 40


def validate(line: str) -> None:
    if not line.strip():
        raise ValueError("entry line is blank")
    if len(line) != len(line.strip()):
        raise ValueError("entry line has leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry line is {len(line)} chars, over {MAX_CHARS}")
    words = line.split()
    if not MIN_WORDS <= len(words) <= MAX_WORDS:
        raise ValueError(f"entry line has {len(words)} words, outside "
                         f"{MIN_WORDS}-{MAX_WORDS}")
    line.encode("utf-8")  # must be valid UTF-8 text


def main() -> int:
    validate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)

    # Read-back check: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != LINE:
        raise ValueError("read-back mismatch: entry.txt differs from LINE")
    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
