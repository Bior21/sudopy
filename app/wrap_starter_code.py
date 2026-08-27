"""Wraps every problem's starter_code in a function prototype.

A one-time migration script that rewrites every content/**/*.json
problem file so its starter_code becomes a `def something():` prototype
around the original starter code, with a call to something() appended.
This is purely a starter-code presentation change - grading is
untouched, since runner.py still executes the whole file as a plain
script and grader.py still compares stdout, because the function is
called at the bottom. Solving a problem still means writing
input()/print() code, just inside the something() body instead of at the
top level. Run once with `python3 wrap_starter_code.py`; safe to re-run,
since it detects already-wrapped starter_code and skips it.
"""

import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"


def wrap(starter_code: str) -> str:
    """Wraps flat starter_code in a def something(): stub.

    Args:
        starter_code: The problem's current starter_code value.

    Returns:
        The wrapped starter_code, or the original unchanged if it was
        already wrapped.
    """
    if starter_code.lstrip().startswith("def something("):
        return starter_code  # already wrapped, don't double-wrap

    lines = starter_code.rstrip("\n").split("\n")
    indented = "\n".join(("    " + line if line.strip() else "") for line in lines)
    return f"def something():\n{indented}\n\nsomething()\n"


def main():
    """Wraps starter_code in every content/**/*.json file that isn't already wrapped."""
    json_files = sorted(CONTENT_DIR.rglob("*.json"))
    changed = 0

    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        original = data["starter_code"]
        wrapped = wrap(original)

        if wrapped != original:
            data["starter_code"] = wrapped
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            changed += 1

    print(f"Wrapped starter_code in {changed}/{len(json_files)} problem files.")


if __name__ == "__main__":
    main()
