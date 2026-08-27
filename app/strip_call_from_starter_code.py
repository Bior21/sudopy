"""Strips the trailing function call from every problem's starter_code.

A one-time migration script that removes the trailing
"\n\nsomething()\n" call from every problem's starter_code, leaving just
the function prototype. The call is no longer part of what the student
sees or edits - instead, core/submission.py appends it automatically
before running, which means a student can never accidentally delete the
call and be confused about why nothing happens. Safe to re-run: skips
files that don't already end with the call.
"""

import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

CALL_SUFFIX = "\n\nsomething()\n"


def strip_call(starter_code: str) -> str:
    """Removes the trailing function-call line from starter_code, if present.

    Args:
        starter_code: The problem's current starter_code value.

    Returns:
        The starter_code with the trailing call removed, or unchanged if
        it didn't end with the call.
    """
    if starter_code.endswith(CALL_SUFFIX):
        return starter_code[: -len(CALL_SUFFIX)] + "\n"
    return starter_code


def main():
    """Strips the trailing call from starter_code in every content/**/*.json file."""
    json_files = sorted(CONTENT_DIR.rglob("*.json"))
    changed = 0

    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        original = data["starter_code"]
        stripped = strip_call(original)

        if stripped != original:
            data["starter_code"] = stripped
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            changed += 1

    print(f"Stripped call from {changed}/{len(json_files)} problem files.")


if __name__ == "__main__":
    main()
