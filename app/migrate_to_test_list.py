"""Migrates every problem's test_input/expected_output into a tests list.

A one-time migration script that rewrites every content/**/*.json problem
file, replacing its top-level `test_input` and `expected_output` fields
with `tests: [{"input": test_input, "expected_output": expected_output}]`.
This lets a problem carry more than one test case - grading now runs the
submission once per entry in `tests` instead of exactly once - while
preserving every problem's existing single test case as tests[0]. Safe
to re-run: skips files that already have a `tests` field.
"""

import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"


def migrate(data: dict) -> dict:
    """Converts one problem's parsed JSON from the old schema to the new one.

    Args:
        data: The problem's parsed JSON, in the old test_input/
            expected_output schema.

    Returns:
        The same dict, with test_input/expected_output replaced by a
        tests list. Left unchanged if "tests" is already present.
    """
    if "tests" in data:
        return data

    test_input = data.pop("test_input", "")
    expected_output = data.pop("expected_output")
    data["tests"] = [{"input": test_input, "expected_output": expected_output}]
    return data


def main():
    """Migrates every content/**/*.json file that hasn't been migrated yet."""
    json_files = sorted(CONTENT_DIR.rglob("*.json"))
    changed = 0

    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        migrated = migrate(dict(data))

        if migrated != data:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(migrated, f, indent=2)
            changed += 1

    print(f"Migrated {changed}/{len(json_files)} problem files to the tests list schema.")


if __name__ == "__main__":
    main()
