"""Lints the entire content/ directory before packaging.

A standalone CLI script that catches malformed JSON, missing required
fields, duplicate problem ids across the whole content set, a topic
folder whose internal "topic" field doesn't match its folder name, and
empty topic folders (reported as a warning, not an error). Run with
`python validate_content.py [path_to_content_dir]`; exits with status 1
if any errors were found, which makes it usable as a CI check.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from core.problem_loader import ProblemLoader, ProblemValidationError, REQUIRED_FIELDS


def _validate_problem_file(
    json_file: Path, expected_topic: str, seen_ids: dict[str, Path]
) -> tuple[list[str], list[str]]:
    """Validates one problem JSON file.

    Records the file's id into seen_ids (shared across the whole content
    set) so later calls can detect duplicates.

    Args:
        json_file: The problem file to validate.
        expected_topic: The topic name implied by the file's parent folder.
        seen_ids: A mapping from problem id to the file it was first seen
            in, updated in place as ids are discovered.

    Returns:
        A tuple of (errors, warnings) as lists of human-readable messages.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{json_file}: invalid JSON ({e})")
        return errors, warnings

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        errors.append(f"{json_file}: missing field(s) {sorted(missing)}")
        return errors, warnings

    if data["topic"] != expected_topic:
        errors.append(
            f"{json_file}: 'topic' field is '{data['topic']}' but folder "
            f"implies '{expected_topic}'"
        )

    problem_id = data["id"]
    if problem_id in seen_ids:
        errors.append(
            f"{json_file}: duplicate id '{problem_id}' "
            f"(already used in {seen_ids[problem_id]})"
        )
    else:
        seen_ids[problem_id] = json_file

    if not data["expected_output"].strip() and not data.get("test_input", "").strip():
        warnings.append(f"{json_file}: expected_output is empty - is this intentional?")

    return errors, warnings


def validate(content_dir: Path) -> tuple[list[str], list[str]]:
    """Lints every problem file under content_dir.

    Checks for malformed JSON, missing required fields, duplicate problem
    ids, a topic field that doesn't match its folder name, and empty
    topic folders.

    Args:
        content_dir: The content directory to validate.

    Returns:
        A tuple of (errors, warnings) as lists of human-readable messages.
    """
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, Path] = {}

    if not content_dir.exists():
        errors.append(f"Content directory not found: {content_dir}")
        return errors, warnings

    topic_folders = sorted(path for path in content_dir.iterdir() if path.is_dir())

    for folder in topic_folders:
        expected_topic = ProblemLoader._strip_numeric_prefix(folder.name)
        json_files = sorted(folder.glob("*.json"))

        if not json_files:
            warnings.append(f"Empty topic folder (no problems yet): {folder.name}")
            continue

        for json_file in json_files:
            file_errors, file_warnings = _validate_problem_file(
                json_file, expected_topic, seen_ids
            )
            errors.extend(file_errors)
            warnings.extend(file_warnings)

    return errors, warnings


def main():
    """Validates content/ (or a path given on the command line) and reports results.

    Exits with status 1 if any errors were found, which makes this usable
    as a CI check.
    """
    content_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "content"

    errors, warnings = validate(content_dir)

    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  ! {warning}")
        print()

    if errors:
        print(f"Errors ({len(errors)}):")
        for error in errors:
            print(f"  x {error}")
        print(f"\nFAILED: {len(errors)} error(s) found in {content_dir}")
        sys.exit(1)

    print(f"OK: content directory is valid ({content_dir})")
    sys.exit(0)


if __name__ == "__main__":
    main()
