"""Appends the function call to student code before it's run and graded.

Every problem's starter_code is a `def <function_name>(...):` prototype
with no visible call to it - the student only ever writes/edits what's
inside the function body. This module is the single place that knows the
function needs to actually be invoked to produce any output, via
build_executable_code(), run_submission(), and run_and_grade().
function_name is per-problem (e.g. "sum_up_to"), not a fixed generic name
- see Problem.function_name in problem_loader.py. Centralizing the
"append the call" logic here, rather than in gui/problem_view.py, means
any future caller - a CLI grading mode, a batch re-grader, etc. - gets
the same behavior for free instead of re-implementing it and risking drift.

Most problems pass their test data as positional arguments (a
TestCase's `args`), so the appended call is built as
`function_name(*args)` with each argument's real Python repr - a test
case can supply any JSON-representable value: an int, a string, a list,
a dict. A shrinking minority of problems (I/O topic) still read via
input(), passing test data as stdin text (`input`) to a zero-argument
function instead; both are handled here so callers don't need to care
which style a given problem uses.

Grading still works purely on stdout (see core/grader.py), so a solution
that `return`s a value instead of calling print() needs that value to
actually reach stdout - the appended call does this automatically by
printing whatever the function returns, unless it returns None. A
function that already prints its own output and has no explicit return
statement returns None, so this doesn't change anything for it; a
function that instead computes and returns a value gets that value
printed for free, without the student needing to call print() themselves.
"""

from __future__ import annotations

from .problem_loader import TestCase
from .runner import run_code, ExecutionResult
from .grader import grade, GradeResult

_RESULT_VAR = "__sudopy_result"


def build_executable_code(student_code: str, function_name: str, args: list | None = None) -> str:
    """Appends a call to function_name so the student's code actually runs.

    The appended call captures the function's return value and prints it
    if it isn't None, so a solution written with `return` produces stdout
    to grade just like one written with `print()` - see this module's
    docstring for why.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        args: Positional arguments to call it with. Each is inserted into
            the generated source via repr(), so it can be any value a
            JSON test case can express - int, float, str, bool, list, or
            dict. Defaults to no arguments.

    Returns:
        The complete, runnable source code.
    """
    args_source = ", ".join(repr(arg) for arg in (args or []))
    call = (
        f"{_RESULT_VAR} = {function_name}({args_source})\n"
        f"if {_RESULT_VAR} is not None:\n"
        f"    print({_RESULT_VAR})\n"
    )
    return student_code.rstrip("\n") + "\n\n" + call


def run_submission(
    student_code: str, function_name: str, test_input: str = "", args: list | None = None
) -> ExecutionResult:
    """Appends the function call and runs the resulting code.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        test_input: Text fed to the process's stdin, for a problem that
            still reads via input() instead of taking arguments.
        args: Positional arguments to call the function with.

    Returns:
        The ExecutionResult from running the code.
    """
    full_code = build_executable_code(student_code, function_name, args)
    return run_code(full_code, test_input)


def run_and_grade(
    student_code: str,
    function_name: str,
    test_input: str,
    expected_output: str,
    args: list | None = None,
) -> GradeResult:
    """Runs a student's submission and grades its output.

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        test_input: Text fed to the process's stdin, for a problem that
            still reads via input() instead of taking arguments.
        expected_output: The output the problem expects.
        args: Positional arguments to call the function with.

    Returns:
        A GradeResult describing whether the submission passed and why.
    """
    result = run_submission(student_code, function_name, test_input, args)
    return grade(result, expected_output)


def run_and_grade_all(
    student_code: str, function_name: str, tests: list[TestCase]
) -> list[GradeResult]:
    """Runs a student's submission against every one of a problem's test cases.

    The submission is re-run once per test case, since each test case can
    supply different arguments (or different stdin).

    Args:
        student_code: The student's submitted function definition.
        function_name: The name of the function to call after defining it.
        tests: The problem's test cases to run the submission against.

    Returns:
        One GradeResult per test case, in the same order as tests.
    """
    return [
        run_and_grade(student_code, function_name, test.input, test.expected_output, test.args)
        for test in tests
    ]
