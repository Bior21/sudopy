from core.problem_loader import TestCase
from core.submission import build_executable_code, run_submission, run_and_grade, run_and_grade_all


def test_build_executable_code_appends_call_with_correct_name():
    code = "def add_two_numbers():\n    print('hi')\n"
    full = build_executable_code(code, "add_two_numbers")
    assert "add_two_numbers()" in full
    assert "def add_two_numbers():" in full


def test_build_executable_code_prints_a_returned_value():
    code = "def add_two_numbers():\n    return 2 + 2\n"
    full = build_executable_code(code, "add_two_numbers")
    assert "print(" in full


def test_returning_a_value_is_graded_the_same_as_printing_it():
    student_code = "def add_two_numbers():\n    return 2 + 2\n"
    g = run_and_grade(student_code, "add_two_numbers", test_input="", expected_output="4")
    assert g.passed


def test_returning_none_prints_nothing_extra():
    # A function with no explicit return (or `return` with no value)
    # returns None - this must not print the literal word "None".
    student_code = "def greet():\n    print('hi')\n"
    result = run_submission(student_code, "greet")
    assert result.stdout.strip() == "hi"


def test_run_submission_executes_the_function_body():
    code = "def greet():\n    print('hello')\n"
    result = run_submission(code, "greet")
    assert result.stdout.strip() == "hello"
    assert result.succeeded


def test_run_submission_passes_test_input_through():
    code = "def double_it():\n    n = int(input())\n    print(n * 2)\n"
    result = run_submission(code, "double_it", test_input="21")
    assert result.stdout.strip() == "42"


def test_different_problems_can_use_different_function_names():
    code_a = "def sum_of_first_n_numbers():\n    print(15)\n"
    code_b = "def reverse_a_word():\n    print('olleh')\n"

    result_a = run_submission(code_a, "sum_of_first_n_numbers")
    result_b = run_submission(code_b, "reverse_a_word")

    assert result_a.stdout.strip() == "15"
    assert result_b.stdout.strip() == "olleh"


def test_student_never_needs_to_write_the_call_themselves():
    # Simulates exactly what a student sees/edits: the prototype, filled in,
    # with no visible call to the function anywhere.
    student_code = (
        "def sum_of_first_n_numbers():\n"
        "    n = int(input())\n"
        "    total = 0\n"
        "    for i in range(1, n + 1):\n"
        "        total += i\n"
        "    print(total)\n"
    )
    assert "sum_of_first_n_numbers()" not in student_code.replace(
        "def sum_of_first_n_numbers()", ""
    )

    g = run_and_grade(student_code, "sum_of_first_n_numbers", test_input="5", expected_output="15")
    assert g.passed


def test_wrong_solution_fails_gracefully_not_crashes():
    student_code = "def sum_of_first_n_numbers():\n    print(999)\n"
    g = run_and_grade(student_code, "sum_of_first_n_numbers", test_input="5", expected_output="15")
    assert not g.passed
    assert "didn't match" in g.reason.lower()


def test_renaming_the_function_gives_a_clear_error_not_a_silent_failure():
    # If a student renames the function away from what the problem expects,
    # the auto-appended call will NameError - this should surface as a
    # crash with a readable reason, not silently produce no output.
    student_code = "def solve():\n    print('hi')\n"
    g = run_and_grade(student_code, "sum_of_first_n_numbers", test_input="", expected_output="hi")
    assert not g.passed
    assert "error" in g.reason.lower()


def test_run_and_grade_all_checks_every_test_case():
    student_code = "def double_it():\n    n = int(input())\n    print(n * 2)\n"
    tests = [
        TestCase(input="1", expected_output="2"),
        TestCase(input="10", expected_output="20"),
    ]
    results = run_and_grade_all(student_code, "double_it", tests)
    assert len(results) == 2
    assert all(g.passed for g in results)


def test_run_and_grade_all_reports_a_mix_of_pass_and_fail():
    # A solution that's hardcoded to the first test case should fail the
    # second one, not be masked by the first passing.
    student_code = "def double_it():\n    input()\n    print(2)\n"
    tests = [
        TestCase(input="1", expected_output="2"),
        TestCase(input="10", expected_output="20"),
    ]
    results = run_and_grade_all(student_code, "double_it", tests)
    assert results[0].passed
    assert not results[1].passed


def test_run_and_grade_all_preserves_test_order():
    student_code = "def echo():\n    print(input())\n"
    tests = [
        TestCase(input="first", expected_output="first"),
        TestCase(input="second", expected_output="second"),
        TestCase(input="third", expected_output="third"),
    ]
    results = run_and_grade_all(student_code, "echo", tests)
    assert [g.actual_output.strip() for g in results] == ["first", "second", "third"]
