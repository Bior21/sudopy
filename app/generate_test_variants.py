"""Adds extra hand-picked test cases to problems with real input variation.

One-time content-authoring script. Problems whose starter_code reads
dynamic input() get 2 additional test cases beyond their original one,
chosen to cover different values and edge cases (boundaries, zero,
negative numbers, equal values, empty results, etc.) - this is what lets
grading catch a solution that's hardcoded to the one original sample
input rather than actually solving the problem. Problems with no
input() (their data is a fixed literal baked into starter_code, e.g.
most of the tuples/dictionaries/nested problems) are left with just
their one test case, since there's nothing to vary without rewriting the
problem itself.

Expected outputs are computed by actually running each problem's known-
correct solution (from core.solutions.SOLUTIONS) against the new input,
never hand-typed, so a mistake in the input choices below can't silently
corrupt content with a wrong expected_output - a crash or timeout in the
reference solution aborts the whole run instead.

Safe to re-run: skips a problem's extra inputs if they're already present.
"""

import json
from pathlib import Path

from core.runner import run_code
from core.solutions import SOLUTIONS

CONTENT_DIR = Path(__file__).parent / "content"

# Extra inputs per problem id, in the same "one input() call per line"
# shape as that problem's original test case.
EXTRA_INPUTS = {
    "variables_001": ["1", "99"],
    "variables_002": ["1\n2", "10\n-5"],
    "variables_003": ["0", "-3"],
    "variables_004": ["4\n9", "5\n5"],
    "variables_005": ["cat", "encyclopedia"],
    "operators_001": ["3\n3", "10\n7"],
    "operators_002": ["9", "14"],
    "operators_003": ["20\n4", "7\n2"],
    "operators_004": ["3\n2", "5\n0"],
    "operators_005": ["15", "10"],
    "io_001": ["Sam", "Zainab"],
    "io_002": ["cat\ndog", "red\nblue"],
    "io_003": ["apple\norange", "red\nblue"],
    "io_004": ["0.5", "100.0"],
    "io_005": ["Tom\n30", "Zoe\n7"],
    "conditionals_001": ["8", "0"],
    "conditionals_002": ["3\n8", "5\n5"],
    "conditionals_003": ["45", "60"],
    "conditionals_004": ["5", "0"],
    "conditionals_005": ["4", "18"],
    "loops_001": ["1", "10"],
    "loops_002": ["1", "6"],
    "loops_003": ["1", "7"],
    "loops_004": ["1", "20"],
    "strings_001": ["hello", "a"],
    "strings_002": ["world", "a"],
    "strings_003": ["world", "AbC"],
    "strings_004": ["apple", "cucumber"],
    "strings_005": ["cat", "hi"],
    "lists_001": ["10\n20\n30", "0\n0\n0"],
    "lists_002": ["5\n5\n5", "1\n2\n3"],
    "lists_003": ["5\n6\n7\n8", "0\n-1\n2\n-3"],
}


def add_variants_for(problem_id: str, extra_inputs: list[str]) -> int:
    """Adds extra test cases for one problem, if not already present.

    Args:
        problem_id: The problem's id, used to find its content file and
            its solution in SOLUTIONS.
        extra_inputs: The additional inputs to generate test cases for.

    Returns:
        How many test cases were actually added (0 if already present).

    Raises:
        RuntimeError: If the reference solution crashes or times out on
            one of extra_inputs - that means the input choice is bad,
            not that the content should silently get a wrong expected
            output.
    """
    path = next(CONTENT_DIR.rglob(f"{problem_id}.json"))
    data = json.loads(path.read_text(encoding="utf-8"))

    existing_inputs = {test["input"] for test in data["tests"]}
    new_inputs = [i for i in extra_inputs if i not in existing_inputs]
    if not new_inputs:
        return 0

    solution = SOLUTIONS[problem_id]
    for extra_input in new_inputs:
        result = run_code(solution, extra_input)
        if result.crashed or result.timed_out:
            raise RuntimeError(
                f"{problem_id}: reference solution failed on input {extra_input!r}: "
                f"{result.stderr or 'timed out'}"
            )
        data["tests"].append({"input": extra_input, "expected_output": result.stdout.rstrip("\n")})

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return len(new_inputs)


def main():
    """Adds every problem's extra test cases from EXTRA_INPUTS."""
    total_added = 0
    for problem_id, extra_inputs in EXTRA_INPUTS.items():
        added = add_variants_for(problem_id, extra_inputs)
        total_added += added
        print(f"{problem_id}: +{added} test case(s)")

    print(f"\nAdded {total_added} test case(s) across {len(EXTRA_INPUTS)} problem(s).")


if __name__ == "__main__":
    main()
