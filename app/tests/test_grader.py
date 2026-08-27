from core.grader import grade
from core.runner import ExecutionResult


def make_result(stdout="", stderr="", timed_out=False, returncode=0):
    return ExecutionResult(
        stdout=stdout, stderr=stderr, timed_out=timed_out, returncode=returncode
    )


def test_exact_match_passes():
    result = make_result(stdout="15\n")
    g = grade(result, expected_output="15")
    assert g.passed


def test_mismatch_fails():
    result = make_result(stdout="14\n")
    g = grade(result, expected_output="15")
    assert not g.passed


def test_ignores_leading_trailing_whitespace():
    result = make_result(stdout="   15   \n\n")
    g = grade(result, expected_output="15")
    assert g.passed


def test_ignores_trailing_whitespace_per_line():
    result = make_result(stdout="7 3   \n")
    g = grade(result, expected_output="7 3")
    assert g.passed


def test_multiline_output_must_match_order():
    result = make_result(stdout="a\nb\nc\n")
    g = grade(result, expected_output="a\nb\nc")
    assert g.passed

    result2 = make_result(stdout="b\na\nc\n")
    g2 = grade(result2, expected_output="a\nb\nc")
    assert not g2.passed


def test_case_sensitive():
    result = make_result(stdout="Hello\n")
    g = grade(result, expected_output="hello")
    assert not g.passed


def test_timeout_fails_with_clear_reason():
    result = make_result(timed_out=True)
    g = grade(result, expected_output="anything")
    assert not g.passed
    assert "too long" in g.reason.lower()


def test_crash_fails_with_stderr_in_reason():
    result = make_result(stderr="ZeroDivisionError: division by zero", returncode=1)
    g = grade(result, expected_output="anything")
    assert not g.passed
    assert "ZeroDivisionError" in g.reason
