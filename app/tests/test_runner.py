from core.runner import run_code


def test_simple_print():
    result = run_code("print('hello')")
    assert result.stdout.strip() == "hello"
    assert result.succeeded


def test_stdin_is_passed_through():
    code = "name = input()\nprint('hi ' + name)"
    result = run_code(code, stdin_input="world")
    assert result.stdout.strip() == "hi world"
    assert result.succeeded


def test_multiple_input_calls():
    code = "a = int(input())\nb = int(input())\nprint(a + b)"
    result = run_code(code, stdin_input="3\n4")
    assert result.stdout.strip() == "7"


def test_crash_is_captured_not_raised():
    result = run_code("1 / 0")
    assert result.crashed
    assert not result.succeeded
    assert "ZeroDivisionError" in result.stderr


def test_syntax_error_is_captured():
    result = run_code("this is not valid python (((")
    assert result.crashed
    assert "SyntaxError" in result.stderr


def test_infinite_loop_times_out():
    result = run_code("while True:\n    pass", timeout=1)
    assert result.timed_out
    assert not result.succeeded
    assert result.returncode is None


def test_timeout_does_not_hang_test_suite():
    # This test itself should complete quickly - if run_code's timeout
    # mechanism is broken, this test would hang indefinitely.
    import time
    start = time.time()
    run_code("while True:\n    pass", timeout=1)
    elapsed = time.time() - start
    assert elapsed < 5  # generous upper bound, should be ~1s
