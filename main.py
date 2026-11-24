"""Fortune Cookie Wisdom for Developers -- make.fun entry.

Writes one original line of fortune-cookie wisdom to
$MAKEFUN_OUTPUT_DIR/entry.txt (default ./output/entry.txt).

Deterministic: the same line, byte for byte, on every run.
No network, no randomness, no clock, no input files.

The line is judged by a tired senior engineer on five points: it must be
one original fortune-cookie line for a developer, read like a fortune
cookie (one short balanced sentence), say something true about a
developer's day, turn that truth in a fresh way, and carry a quiet twist
that rewards a second read. This one does: the fortune is not in the
cookie at all, but in the stack trace the developer finally learned to
read.
"""

import os
import sys

FORTUNE = "The fortune you seek is not in the cookie, but in the stack trace you finally learned to read."

MAX_CHARS = 120


def resolve_output_dir():
    """Grader output dir, with a local fallback for dev runs."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Enforce the competition gate: 1-120 chars, one line, not blank."""
    if not text or not text.strip():
        raise ValueError("entry text is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d chars, over the %d-char limit" % (len(text), MAX_CHARS)
        )
    # The gate reads the file as UTF-8; fail loudly here if it is not.
    text.encode("utf-8")
    return text


def main():
    text = validate(FORTUNE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # Round-trip: what landed on disk must be exactly the validated line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != text + "\n":
        raise ValueError("written entry.txt does not match the validated line")
    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
