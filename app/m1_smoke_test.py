"""Manually exercises the loader -> runner -> grader pipeline end to end.

Loads all problems from content/, runs each problem's starter_code
(which is intentionally incomplete, so those runs are expected to fail
grading), and also runs a hand-written correct solution for each problem
to prove the pipeline works when the code is correct. Also checks the
runner's timeout and crash handling directly. This is not a pytest suite
- it's a quick manual check, run with `python m1_smoke_test.py`.
"""

from pathlib import Path

from core.problem_loader import ProblemLoader
from core.runner import run_code
from core.grader import grade


CONTENT_DIR = Path(__file__).parent / "content"

# Hand-written correct solutions, keyed by problem id, just for this smoke test
CORRECT_SOLUTIONS = {
    "variables_001": "age = int(input())\nprint(age)\n",
    "variables_002": "a = int(input())\nb = int(input())\na, b = b, a\nprint(a, b)\n",
    "loops_001": (
        "n = int(input())\n"
        "total = 0\n"
        "for i in range(1, n + 1):\n"
        "    total += i\n"
        "print(total)\n"
    ),
}


def main():
    """Runs every problem's starter code and correct solution, and prints the results.

    Also proves the runner's timeout and crash handling work, using a
    hand-written infinite loop and a divide-by-zero. Not a pass/fail
    check - prints results for a human to eyeball.
    """
    loader = ProblemLoader(CONTENT_DIR)
    topics = loader.load_all()

    print(f"Discovered topics: {list(topics.keys())}\n")

    for topic_name, topic in topics.items():
        print(f"=== Topic: {topic_name} ===")
        for problem in topic.problems:
            print(f"  Problem: {problem.id} - {problem.title}")

            # Run the starter code as-is (expected to fail/incomplete)
            starter_result = run_code(problem.starter_code, problem.test_input)
            starter_grade = grade(starter_result, problem.expected_output)
            print(f"    starter_code -> passed={starter_grade.passed} "
                  f"({starter_grade.reason.splitlines()[0]})")

            # Run our hand-written correct solution (expected to pass)
            if problem.id in CORRECT_SOLUTIONS:
                solution_result = run_code(
                    CORRECT_SOLUTIONS[problem.id], problem.test_input
                )
                solution_grade = grade(solution_result, problem.expected_output)
                status = "PASS" if solution_grade.passed else "FAIL <-- unexpected!"
                print(f"    correct_solution -> {status}")
            else:
                print("    (no hand-written solution registered for this id)")
        print()

    # Also prove timeout handling works
    print("=== Timeout check ===")
    infinite_loop_code = "while True:\n    pass\n"
    result = run_code(infinite_loop_code, "", timeout=2)
    result_grade = grade(result, "anything")
    print(f"  infinite loop -> timed_out={result.timed_out}, "
          f"passed={result_grade.passed}, reason={result_grade.reason}")

    # And crash handling
    print("=== Crash check ===")
    crashing_code = "1 / 0\n"
    result = run_code(crashing_code, "")
    result_grade = grade(result, "anything")
    print(f"  divide by zero -> crashed={result.crashed}, "
          f"passed={result_grade.passed}, reason={result_grade.reason.splitlines()[0]}")


if __name__ == "__main__":
    main()
