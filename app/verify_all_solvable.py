"""Confirms every problem in content/ actually has a working solution.

For every problem, runs the hand-written correct solution from
core.solutions.SOLUTIONS and confirms it actually passes grading against
every one of that problem's test cases. This catches authoring mistakes
that JSON-schema validation can't, such as an expected_output that
doesn't match what correct code produces, or a starter_code/test input
mismatch.
"""

from pathlib import Path

from core.problem_loader import ProblemLoader
from core.runner import run_code
from core.grader import grade
from core.solutions import SOLUTIONS


CONTENT_DIR = Path(__file__).parent / "content"


def main():
    """Runs every registered solution against its problem and reports pass/fail.

    Exits with status 1 if any registered solution fails to produce its
    problem's expected_output, which makes this usable as a CI check.
    """
    loader = ProblemLoader(CONTENT_DIR)
    topics = loader.load_all()

    all_ids = [p.id for topic in topics.values() for p in topic.problems]
    missing_solutions = [pid for pid in all_ids if pid not in SOLUTIONS]

    failures = []
    checked = 0

    for topic_name, topic in topics.items():
        for problem in topic.problems:
            if problem.id not in SOLUTIONS:
                continue
            checked += 1
            all_tests_passed = True
            for index, test in enumerate(problem.tests, start=1):
                result = run_code(SOLUTIONS[problem.id], test.input)
                g = grade(result, test.expected_output)
                if not g.passed:
                    all_tests_passed = False
                    failures.append((f"{problem.id} (test {index})", g.reason, result.stdout, test.expected_output))
            status = "PASS" if all_tests_passed else "FAIL"
            print(f"[{status}] {topic_name}/{problem.id} ({len(problem.tests)} test(s))")

    print(f"\nChecked {checked}/{len(all_ids)} problems.")

    if missing_solutions:
        print(f"\nNo solution registered for: {missing_solutions}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for pid, reason, actual, expected in failures:
            print(f"  {pid}: {reason}")
            print(f"    actual:   {actual!r}")
            print(f"    expected: {expected!r}")
        raise SystemExit(1)

    print("\nAll problems with registered solutions PASSED.")


if __name__ == "__main__":
    main()
