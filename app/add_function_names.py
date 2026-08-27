"""Derives and assigns a unique function_name for every problem.

A one-time migration script that derives a snake_case function_name from
each problem's title (e.g. "Sum of first N numbers" ->
"sum_of_first_n_numbers"), adds it to the JSON schema, and rewrites
starter_code's "def something():" line to use that name instead. It
verifies uniqueness across the whole content set, since two problems
landing on the same derived name would silently make one of them
ungradeable in a confusing way, so it fails loudly instead if that ever
happens. Safe to re-run: if function_name is already present and
starter_code already uses it, the file is left untouched.
"""

import json
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

OLD_DEF_LINE = "def something():"


def slugify(title: str) -> str:
    """Converts a problem title into a snake_case function name.

    Args:
        title: The problem's title, e.g. "Sum of first N numbers".

    Returns:
        A snake_case slug, e.g. "sum_of_first_n_numbers".
    """
    name = title.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def main():
    """Assigns a unique function_name to every problem, derived from its title.

    Raises:
        SystemExit: If two problems' titles slugify to the same function
            name.
    """
    json_files = sorted(CONTENT_DIR.rglob("*.json"))
    changed = 0
    seen_names: dict[str, Path] = {}

    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        function_name = slugify(data["title"])

        if function_name in seen_names:
            raise SystemExit(
                f"Function name collision: '{function_name}' derived from both "
                f"{seen_names[function_name]} and {path}. Rename one problem's title."
            )
        seen_names[function_name] = path

        new_starter_code = data["starter_code"].replace(
            OLD_DEF_LINE, f"def {function_name}():"
        )

        needs_write = (
            data.get("function_name") != function_name
            or new_starter_code != data["starter_code"]
        )

        if needs_write:
            data["function_name"] = function_name
            data["starter_code"] = new_starter_code
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            changed += 1

    print(f"Assigned/updated function_name in {changed}/{len(json_files)} problem files.")
    print(f"All {len(seen_names)} function names are unique.")


if __name__ == "__main__":
    main()
