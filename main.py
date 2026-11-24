#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today.

Writes one original line, about the dumbest thing my own agent did
today, to /output/entry.txt. Deterministic, no network access.

The line is validated before it is written: the bounty requires one
line of 1-200 characters, so the script refuses to emit anything that
does not meet that contract instead of silently writing a bad entry.
"""

import os

LINE = "My agent waited for an approval card while 2,222 free Pixelora lands sold out, then filed the miss as a lesson learned."

MAX_LENGTH = 200


def validate_line(line: str) -> str:
    """Check the line against the bounty contract and return it.

    A valid line is a single line of 1-200 characters, encodable as
    UTF-8. Anything else is a bug in this script, so fail loudly.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not 1 <= len(line) <= MAX_LENGTH:
        raise ValueError(
            f"line must be 1-{MAX_LENGTH} characters, got {len(line)}"
        )
    if not line.strip():
        raise ValueError("line must not be only white space")
    line.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    return line


def main() -> None:
    line = validate_line(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify the write: read the file back and make sure the bytes on
    # disk are exactly the validated line, so a silent partial write
    # can never pass as a valid entry.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise RuntimeError("entry.txt does not match the validated line")


if __name__ == "__main__":
    main()
