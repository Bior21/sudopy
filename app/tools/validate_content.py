"""
File: validate_content.py
Author: Bior Madol Khom Bior
----------------------------
Checks every problem file for mistakes before the app is packaged:
broken JSON, missing fields, two problems with the same id, and a
"topic" that doesn't match the problem's folder. Run it from inside app/:

    python3 -m tools.validate_content

It exits with status 1 if it finds an error, so CI can use it as a check.
"""

import json
import sys
from pathlib import Path

from core.problem_loader import REQUIRED_FIELDS, topic_name_from_folder

CONTENT_DIR = Path(__file__).parent.parent / "content"


def check_problem_file(path: Path, folder_topic: str, seen_ids: dict) -> list[str]:
    """
    Returns a list of everything wrong with one problem file. seen_ids maps
    each id found so far to its file, and is used to spot duplicate ids.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        return [f"{path}: invalid JSON ({error})"]

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return [f"{path}: missing field(s) {sorted(missing)}"]

    errors = []
    if data["topic"] != folder_topic:
        errors.append(f"{path}: 'topic' is '{data['topic']}' but the folder says '{folder_topic}'")

    if data["id"] in seen_ids:
        errors.append(f"{path}: id '{data['id']}' is already used in {seen_ids[data['id']]}")
    else:
        seen_ids[data["id"]] = path

    if not data["tests"]:
        errors.append(f"{path}: 'tests' must not be empty")
    for index, test in enumerate(data["tests"]):
        if "expected_output" not in test:
            errors.append(f"{path}: tests[{index}] is missing 'expected_output'")
    return errors


def main():
    """Checks every problem file and prints any errors found."""
    errors = []
    seen_ids = {}
    for folder in sorted(CONTENT_DIR.iterdir()):
        if not folder.is_dir():
            continue
        json_files = sorted(folder.glob("*.json"))
        if not json_files:
            print(f"Warning: {folder.name} has no problems yet")
        for path in json_files:
            errors.extend(check_problem_file(path, topic_name_from_folder(folder.name), seen_ids))

    if errors:
        for error in errors:
            print(f"  x {error}")
        print(f"\nFAILED: {len(errors)} error(s)")
        sys.exit(1)
    print(f"OK: all {len(seen_ids)} problems are valid")


if __name__ == "__main__":
    main()
