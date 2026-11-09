"""
File: verify_all_solvable.py
Author: Bior Madol Khom Bior
----------------------------
Runs every problem's own solution through the same grading a student's
code goes through, and checks that it passes every test. This catches
mistakes that validate_content.py can't, such as an expected output that
doesn't match what correct code prints. Run it from inside app/:

    python3 -m tools.verify_all_solvable

It exits with status 1 if any solution fails.
"""

import sys
from pathlib import Path

from core.problem_loader import ProblemLoader
from core.submission import run_and_grade_all

CONTENT_DIR = Path(__file__).parent.parent / "content"


def main():
    """Grades every solution and prints PASS or FAIL for each problem."""
    topics = ProblemLoader(CONTENT_DIR).load_all()
    failures = []
    checked = 0

    for topic in topics.values():
        for problem in topic.problems:
            checked += 1
            results = run_and_grade_all(problem.solution, problem.function_name, problem.tests)
            all_passed = True
            for number, result in enumerate(results, start=1):
                if not result.passed:
                    all_passed = False
                    failures.append(f"{problem.id} (test {number}): {result.reason}\n"
                                    f"    got:      {result.actual_output!r}\n"
                                    f"    expected: {result.expected_output!r}")
            status = "PASS" if all_passed else "FAIL"
            print(f"[{status}] {topic.name}/{problem.id}")

    print(f"\nChecked {checked} problems.")
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for failure in failures:
            print(f"  {failure}")
        sys.exit(1)
    print("All solutions passed.")


if __name__ == "__main__":
    main()
