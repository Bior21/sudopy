"""Grades a student's code output against a problem's expected output.

Compares the output of a student's code run (a runner.ExecutionResult)
against a problem's expected_output via the grade() function, which
returns a GradeResult with a pass/fail verdict and a human-readable
reason. Grading works purely on stdout text, not return values, so the
grader doesn't need to import or execute student code as a module -
runner.py already ran it as a standalone script and captured stdout.
"""

from __future__ import annotations

from dataclasses import dataclass

from .runner import ExecutionResult


@dataclass
class GradeResult:
    passed: bool
    reason: str
    actual_output: str
    expected_output: str


def grade(result: ExecutionResult, expected_output: str) -> GradeResult:
    """Grades an ExecutionResult against a problem's expected output.

    Comparison is deliberately lenient for beginners: leading/trailing
    whitespace on the whole output and trailing whitespace per line are
    ignored, but otherwise the match must be exact (case-sensitive,
    order-sensitive).

    Args:
        result: The ExecutionResult produced by running the student's code.
        expected_output: The output the problem expects.

    Returns:
        A GradeResult describing whether the submission passed and why.
    """
    if result.timed_out:
        return GradeResult(
            passed=False,
            reason="Your code took too long to run (possible infinite loop).",
            actual_output=result.stdout,
            expected_output=expected_output,
        )

    if result.crashed:
        return GradeResult(
            passed=False,
            reason=f"Your code crashed with an error:\n{result.stderr.strip()}",
            actual_output=result.stdout,
            expected_output=expected_output,
        )

    actual_normalized = _normalize(result.stdout)
    expected_normalized = _normalize(expected_output)

    if actual_normalized == expected_normalized:
        return GradeResult(
            passed=True,
            reason="Correct!",
            actual_output=result.stdout,
            expected_output=expected_output,
        )

    return GradeResult(
        passed=False,
        reason="Output didn't match expected output.",
        actual_output=result.stdout,
        expected_output=expected_output,
    )


def _normalize(text: str) -> str:
    """Strips leading/trailing blank lines and trailing whitespace per line.

    Args:
        text: The raw output text to normalize.

    Returns:
        The normalized text.
    """
    lines = text.strip("\n").splitlines()
    return "\n".join(line.rstrip() for line in lines).strip()
