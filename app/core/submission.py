"""Appends the function call to student code before it's run and graded.

Every problem's starter_code is a `def <function_name>():` prototype with
no visible call to it - the student only ever writes/edits what's inside
the function body. This module is the single place that knows the
function needs to actually be invoked to produce any output, via
build_executable_code(), run_submission(), and run_and_grade().
function_name is per-problem (e.g. "sum_of_first_n_numbers"), not a fixed
generic name - see Problem.function_name in problem_loader.py.
Centralizing the "append the call" logic here, rather than in
gui/problem_view.py, means any future caller - a CLI grading mode, a
batch re-grader, etc. - gets the same behavior for free instead of
re-implementing it and risking drift.
"""

from __future__ import annotations

from .runner import run_code, ExecutionResult
from .grader import grade, GradeResult


def build_executable_code(student_code: str, function_name: str) -> str:
    """Appends a call to function_name so the student's code actually runs.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.

    Returns:
        The complete, runnable source code.
    """
    return student_code.rstrip("\n") + f"\n\n{function_name}()\n"


def run_submission(student_code: str, function_name: str, test_input: str = "") -> ExecutionResult:
    """Appends the function call and runs the resulting code.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        test_input: Text fed to the process's stdin.

    Returns:
        The ExecutionResult from running the code.
    """
    full_code = build_executable_code(student_code, function_name)
    return run_code(full_code, test_input)


def run_and_grade(
    student_code: str, function_name: str, test_input: str, expected_output: str
) -> GradeResult:
    """Runs a student's submission and grades its output.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        test_input: Text fed to the process's stdin.
        expected_output: The output the problem expects.

    Returns:
        A GradeResult describing whether the submission passed and why.
    """
    result = run_submission(student_code, function_name, test_input)
    return grade(result, expected_output)
