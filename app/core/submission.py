"""
File: submission.py
Author: Bior Madol Khom Bior
----------------------------
Turns a student's function into a program that can be run and graded.
Students only write the function itself, so before running it we add a
line that calls it with the test's arguments and prints whatever it
returns. That way a student may either print the answer or return it.

Most problems pass test data as arguments. The Input/Output problems
instead type the test data in for input() to read.
"""

from .grader import GradeResult, grade
from .problem_loader import TestCase
from .runner import ExecutionResult, run_code

SKIPPED_REASON = "Not run, because an earlier test took too long."


def build_executable_code(student_code: str, function_name: str, args: list | None = None) -> str:
    """
    Adds a call to the student's function after their code, for example:

        result = add(2, 3)
        if result is not None:
            print(result)

    Each argument is written with repr(), so strings keep their quotes.
    """
    if args is None:
        args = []
    arg_texts = []
    for arg in args:
        arg_texts.append(repr(arg))

    call = (
        f"__sudopy_result = {function_name}({', '.join(arg_texts)})\n"
        f"if __sudopy_result is not None:\n"
        f"    print(__sudopy_result)\n"
    )
    return student_code.rstrip("\n") + "\n\n" + call


def run_submission(student_code: str, function_name: str, test_input: str = "",
                   args: list | None = None) -> ExecutionResult:
    """Adds the function call to the student's code and runs it."""
    full_code = build_executable_code(student_code, function_name, args)
    return run_code(full_code, test_input)


def run_and_grade(student_code: str, function_name: str, test_input: str,
                  expected_output: str, args: list | None = None) -> GradeResult:
    """Runs the student's code once and grades what it printed."""
    result = run_submission(student_code, function_name, test_input, args)
    return grade(result, expected_output)


def run_and_grade_all(student_code: str, function_name: str, tests: list[TestCase]) -> list[GradeResult]:
    """
    Runs the student's code once per test case and returns one GradeResult
    per test, in order. If a test times out (probably an infinite loop), the
    remaining tests are marked as skipped instead of each waiting for their
    own timeout.
    """
    results = []
    timed_out = False
    for test in tests:
        if timed_out:
            results.append(GradeResult(False, SKIPPED_REASON, "", test.expected_output))
            continue
        result = run_and_grade(student_code, function_name, test.input, test.expected_output, test.args)
        results.append(result)
        if result.timed_out:
            timed_out = True
    return results
