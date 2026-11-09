"""
File: grader.py
Author: Bior Madol Khom Bior
----------------------------
Checks whether a student's code printed the right answer. Grading only
compares printed output (stdout), so the grader never runs any code
itself; runner.py has already done that.
"""

from dataclasses import dataclass

from .runner import ExecutionResult


@dataclass
class GradeResult:
    passed: bool
    reason: str            # the message shown to the student
    actual_output: str
    expected_output: str
    timed_out: bool = False


def grade(result: ExecutionResult, expected_output: str) -> GradeResult:
    """
    Grades one run of the student's code against the expected output.
    Checks for a timeout first, then a crash, then compares the output.
    """
    if result.timed_out:
        reason = "Your code took too long to run (possible infinite loop)."
        return GradeResult(False, reason, result.stdout, expected_output, timed_out=True)

    if result.crashed:
        reason = "Your code crashed with an error:\n" + result.stderr.strip()
        return GradeResult(False, reason, result.stdout, expected_output)

    if clean_output(result.stdout) == clean_output(expected_output):
        return GradeResult(True, "Correct!", result.stdout, expected_output)

    reason = "Output didn't match expected output."
    return GradeResult(False, reason, result.stdout, expected_output)


def clean_output(text: str) -> str:
    """
    Makes the comparison forgiving for beginners: ignores blank lines and
    spaces at the start and end, and spaces at the end of each line.
    Everything else must match exactly, including capital letters.
    """
    cleaned_lines = []
    for line in text.strip().splitlines():
        cleaned_lines.append(line.rstrip())
    return "\n".join(cleaned_lines)
