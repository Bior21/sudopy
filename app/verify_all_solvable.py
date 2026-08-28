"""Confirms every problem in content/ actually has a working solution.

For every problem, runs the hand-written correct solution from
core.solutions.SOLUTIONS and confirms it actually passes grading against
every one of that problem's test cases. This catches authoring mistakes
that JSON-schema validation can't, such as an expected_output that
doesn't match what correct code produces, or a starter_code/test input
mismatch.

A solution is verified one of two ways, detected from its own shape:
a function-based solution (starts with "def ") is run through
core.submission.run_and_grade_all, the exact same path a real student
submission takes, since these solutions take arguments via a test
case's `args`. A legacy plain-script solution (the original I/O-style
content) is run directly through core.runner.run_code with each test
case's `input`, since it was never written to be called as a function.
"""

from pathlib import Path

from core.problem_loader import ProblemLoader
from core.runner import run_code
from core.grader import grade
from core.solutions import SOLUTIONS
from core.submission import run_and_grade_all


CONTENT_DIR = Path(__file__).parent / "content"


def _verify_problem(problem) -> list:
    """Grades a problem's registered solution against every one of its tests.

    Args:
        problem: The core.problem_loader.Problem to verify.

    Returns:
        A list of core.grader.GradeResult, one per test case.
    """
    solution = SOLUTIONS[problem.id]
    if solution.lstrip().startswith("def "):
        return run_and_grade_all(solution, problem.function_name, problem.tests)
    return [grade(run_code(solution, test.input), test.expected_output) for test in problem.tests]


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
            grade_results = _verify_problem(problem)
            all_tests_passed = all(g.passed for g in grade_results)
            for index, (test, g) in enumerate(zip(problem.tests, grade_results), start=1):
                if not g.passed:
                    failures.append(
                        (f"{problem.id} (test {index})", g.reason, g.actual_output, test.expected_output)
                    )
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
