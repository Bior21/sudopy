"""One-time authoring script: writes the redesigned Loops topic content.

Replaces the old input()-based loops_001..004 with 20 parameter-based
problems (loops_001..020) plus 4 "debug it" problems (loops_debug_001..
004) that ship with near-complete but broken starter_code instead of a
TODO stub.

Every expected_output is computed by actually running a correct,
function-based reference solution through core.submission - never hand-
typed. Every debug problem's buggy starter_code is also run through the
same pipeline and checked to genuinely fail at least one test, so a
"bug" that doesn't actually reproduce can't slip into shipped content.
"""

import json
from pathlib import Path

from core.submission import run_and_grade_all
from core.problem_loader import TestCase

CONTENT_DIR = Path(__file__).parent / "content" / "05_loops"

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "loops_001", "sum_of_odd_numbers_up_to",
        "Given a positive int n, return the sum of just the odd numbers from 1 to n. "
        "e.g. n=6 returns 9 (1+3+5). Use a for/i/range loop.",
        "def sum_of_odd_numbers_up_to(n):\n"
        "    total = 0\n"
        "    for i in range(1, n + 1):\n"
        "        if i % 2 == 1:\n"
        "            total += i\n"
        "    return total\n",
        [[6], [1], [10]],
        "",
    ),
    (
        "loops_002", "count_divisible_by",
        "Given a positive int n and a positive int divisor, return how many numbers from "
        "1 to n are evenly divisible by divisor. e.g. n=10, divisor=3 returns 3 (3, 6, 9).",
        "def count_divisible_by(n, divisor):\n"
        "    count = 0\n"
        "    for i in range(1, n + 1):\n"
        "        if i % divisor == 0:\n"
        "            count += 1\n"
        "    return count\n",
        [[10, 3], [7, 2], [20, 5]],
        "",
    ),
    (
        "loops_003", "sum_of_range",
        "Given two ints start and end, return the sum of every number from start through "
        "end, inclusive. e.g. start=3, end=6 returns 18 (3+4+5+6).",
        "def sum_of_range(start, end):\n"
        "    total = 0\n"
        "    for i in range(start, end + 1):\n"
        "        total += i\n"
        "    return total\n",
        [[3, 6], [5, 5], [1, 10]],
        "",
    ),
    (
        "loops_004", "multiplication_table",
        "Given an int n, return a list of n times 1 through n times 5. "
        "e.g. n=4 returns [4, 8, 12, 16, 20]. Use a for/i/range loop.",
        "def multiplication_table(n):\n"
        "    table = []\n"
        "    for i in range(1, 6):\n"
        "        table.append(n * i)\n"
        "    return table\n",
        [[4], [1], [7]],
        "",
    ),
    (
        "loops_005", "countdown_by_step",
        "Given a non-negative int n and a positive int step, return a list counting down "
        "from n to 0 (or as close to 0 as step allows) in increments of step. "
        "e.g. n=10, step=3 returns [10, 7, 4, 1]. Use a while loop.",
        "def countdown_by_step(n, step):\n"
        "    result = []\n"
        "    current = n\n"
        "    while current >= 0:\n"
        "        result.append(current)\n"
        "        current -= step\n"
        "    return result\n",
        [[10, 3], [5, 5], [6, 2]],
        "",
    ),
    (
        "loops_006", "factorial",
        "Given a non-negative int n, return n factorial (n! = n * (n-1) * ... * 1, "
        "and 0! = 1). e.g. n=5 returns 120.",
        "def factorial(n):\n"
        "    total = 1\n"
        "    for i in range(1, n + 1):\n"
        "        total *= i\n"
        "    return total\n",
        [[5], [0], [7]],
        "",
    ),
    (
        "loops_007", "digit_sum",
        "Given a non-negative int n, return the sum of its digits. e.g. n=493 returns "
        "16 (4+9+3). Use a while loop \u2014 peel off one digit at a time with % and //.",
        "def digit_sum(n):\n"
        "    total = 0\n"
        "    while n > 0:\n"
        "        total += n % 10\n"
        "        n //= 10\n"
        "    return total\n",
        [[493], [7], [1000]],
        "",
    ),
    (
        "loops_008", "count_digits",
        "Given a positive int n, return how many digits it has. e.g. n=4021 returns 4.",
        "def count_digits(n):\n"
        "    count = 0\n"
        "    while n > 0:\n"
        "        count += 1\n"
        "        n //= 10\n"
        "    return count\n",
        [[4021], [7], [1000000]],
        "",
    ),
    (
        "loops_009", "reverse_number",
        "Given a non-negative int n, return it with its digits reversed. "
        "e.g. n=1234 returns 4321. Use a while loop, the same digit-peeling idea as digit_sum.",
        "def reverse_number(n):\n"
        "    reversed_n = 0\n"
        "    while n > 0:\n"
        "        digit = n % 10\n"
        "        reversed_n = reversed_n * 10 + digit\n"
        "        n //= 10\n"
        "    return reversed_n\n",
        [[1234], [7], [1200]],
        "",
    ),
    (
        "loops_010", "number_triangle",
        "Given a positive int n, return a string with n lines, where line i lists the "
        "numbers 1 through i separated by spaces. e.g. n=3 returns '1\\n1 2\\n1 2 3'.",
        "def number_triangle(n):\n"
        "    rows = []\n"
        "    for i in range(1, n + 1):\n"
        "        row = ''\n"
        "        for x in range(1, i + 1):\n"
        "            if x > 1:\n"
        "                row = row + ' '\n"
        "            row = row + str(x)\n"
        "        rows.append(row)\n"
        "    return '\\n'.join(rows)\n",
        [[3], [1], [5]],
        "",
    ),
    (
        "loops_011", "count_vowels",
        "Given a string word, return how many of its characters are vowels "
        "(a, e, i, o, u \u2014 either case). e.g. word='Banana' returns 3. "
        "Use a for-each loop \u2014 for ch in word.",
        "def count_vowels(word):\n"
        "    vowels = 'aeiouAEIOU'\n"
        "    count = 0\n"
        "    for ch in word:\n"
        "        if ch in vowels:\n"
        "            count += 1\n"
        "    return count\n",
        [["Banana"], ["rhythm"], ["EEEasy"]],
        "",
    ),
    (
        "loops_012", "count_occurrences",
        "Given a string word and a single-character string letter, return how many times "
        "letter appears in word. e.g. word='mississippi', letter='s' returns 4. "
        "Use a for-each loop.",
        "def count_occurrences(word, letter):\n"
        "    count = 0\n"
        "    for ch in word:\n"
        "        if ch == letter:\n"
        "            count += 1\n"
        "    return count\n",
        [["mississippi", "s"], ["banana", "a"], ["hello", "z"]],
        "",
    ),
    (
        "loops_013", "sum_of_multiples_of_either",
        "Given a positive int limit and two positive ints a and b, return the sum of "
        "every number below limit that's a multiple of a or b (don't count any number "
        "twice). e.g. limit=20, a=3, b=5 returns 78.",
        "def sum_of_multiples_of_either(limit, a, b):\n"
        "    total = 0\n"
        "    for i in range(1, limit):\n"
        "        if i % a == 0 or i % b == 0:\n"
        "            total += i\n"
        "    return total\n",
        [[20, 3, 5], [10, 2, 3], [15, 5, 5]],
        "",
    ),
    (
        "loops_014", "power_without_operator",
        "Given an int base and a non-negative int exp, return base to the power of exp "
        "\u2014 but compute it by multiplying in a loop, not with **. "
        "e.g. base=2, exp=5 returns 32.",
        "def power_without_operator(base, exp):\n"
        "    result = 1\n"
        "    for i in range(exp):\n"
        "        result *= base\n"
        "    return result\n",
        [[2, 5], [3, 0], [5, 3]],
        "",
    ),
    (
        "loops_015", "is_prime",
        "Given an int n, return whether it's prime (has no divisors other than 1 and "
        "itself; numbers less than 2 are not prime). e.g. n=17 returns True, "
        "n=18 returns False.",
        "def is_prime(n):\n"
        "    if n < 2:\n"
        "        return False\n"
        "    for i in range(2, n):\n"
        "        if n % i == 0:\n"
        "            return False\n"
        "    return True\n",
        [[17], [18], [2]],
        "",
    ),
    (
        "loops_016", "gcd_of_two",
        "Given two positive ints a and b, return their greatest common divisor. "
        "e.g. a=48, b=18 returns 6. Use a while loop \u2014 the classic Euclidean algorithm: "
        "repeatedly replace the larger number with the remainder of dividing by the smaller.",
        "def gcd_of_two(a, b):\n"
        "    while b != 0:\n"
        "        a, b = b, a % b\n"
        "    return a\n",
        [[48, 18], [17, 5], [20, 30]],
        "",
    ),
    (
        "loops_017", "fibonacci_at",
        "Given a positive int n, return the nth Fibonacci number "
        "(1, 1, 2, 3, 5, 8, ... starting at n=1). e.g. n=6 returns 8.",
        "def fibonacci_at(n):\n"
        "    a, b = 0, 1\n"
        "    for i in range(n):\n"
        "        a, b = b, a + b\n"
        "    return a\n",
        [[6], [1], [10]],
        "",
    ),
    (
        "loops_018", "digital_root",
        "Given a positive int n, sum its digits, then keep summing the digits of the "
        "result until only one digit is left, and return it. e.g. n=9875 returns 2 "
        "(9+8+7+5=29, 2+9=11, 1+1=2). Use a while loop \u2014 you don't know how many "
        "rounds it'll take in advance.",
        "def digital_root(n):\n"
        "    while n >= 10:\n"
        "        total = 0\n"
        "        while n > 0:\n"
        "            total += n % 10\n"
        "            n //= 10\n"
        "        n = total\n"
        "    return n\n",
        [[9875], [5], [999]],
        "",
    ),
    (
        "loops_019", "triangle_pattern",
        "Given a positive int n, return a string of n lines, where line i is i asterisks. "
        "e.g. n=4 returns '*\\n**\\n***\\n****'.",
        "def triangle_pattern(n):\n"
        "    rows = []\n"
        "    for i in range(1, n + 1):\n"
        "        rows.append('*' * i)\n"
        "    return '\\n'.join(rows)\n",
        [[4], [1], [6]],
        "",
    ),
    (
        "loops_020", "collatz_steps",
        "Given a positive int n, return how many steps it takes to reach 1 using the "
        "Collatz rule: if n is even, divide it by 2; if it's odd, multiply by 3 and add 1. "
        "e.g. n=6 returns 8. Use a while loop \u2014 it runs until n reaches 1, however long "
        "that takes.",
        "def collatz_steps(n):\n"
        "    steps = 0\n"
        "    while n != 1:\n"
        "        if n % 2 == 0:\n"
        "            n = n // 2\n"
        "        else:\n"
        "            n = 3 * n + 1\n"
        "        steps += 1\n"
        "    return steps\n",
        [[6], [1], [27]],
        "Trace it by hand for a small n first, like 6, so you know what the loop should do each step.",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "loops_debug_001", "sum_of_range",
        "Given start and end, this function is supposed to return the sum of every "
        "number from start through end, inclusive \u2014 but it has a bug. Find it and fix it.",
        "def sum_of_range(start, end):\n"
        "    total = 0\n"
        "    for i in range(start, end + 1):\n"
        "        total += i\n"
        "    return total\n",
        "def sum_of_range(start, end):\n"
        "    total = 0\n"
        "    for i in range(start, end):\n"
        "        total += i\n"
        "    return total\n",
        [[3, 6], [5, 5], [1, 10]],
    ),
    (
        "loops_debug_002", "factorial",
        "Given a non-negative int n, this function is supposed to return n factorial "
        "\u2014 but it has a bug. Find it and fix it.",
        "def factorial(n):\n"
        "    total = 1\n"
        "    for i in range(1, n + 1):\n"
        "        total *= i\n"
        "    return total\n",
        "def factorial(n):\n"
        "    total = 0\n"
        "    for i in range(1, n + 1):\n"
        "        total *= i\n"
        "    return total\n",
        [[5], [1], [7]],
    ),
    (
        "loops_debug_003", "count_divisible_by",
        "Given n and divisor, this function is supposed to count how many numbers from "
        "1 to n are divisible by divisor \u2014 but it has a bug. Find it and fix it.",
        "def count_divisible_by(n, divisor):\n"
        "    count = 0\n"
        "    for i in range(1, n + 1):\n"
        "        if i % divisor == 0:\n"
        "            count += 1\n"
        "    return count\n",
        "def count_divisible_by(n, divisor):\n"
        "    count = 0\n"
        "    for i in range(1, n + 1):\n"
        "        if n % divisor == 0:\n"
        "            count += 1\n"
        "    return count\n",
        [[10, 3], [7, 2], [20, 5]],
    ),
    (
        "loops_debug_004", "is_prime",
        "Given an int n, this function is supposed to return whether n is prime \u2014 "
        "but it has a bug. Find it and fix it.",
        "def is_prime(n):\n"
        "    if n < 2:\n"
        "        return False\n"
        "    for i in range(2, n):\n"
        "        if n % i == 0:\n"
        "            return False\n"
        "    return True\n",
        "def is_prime(n):\n"
        "    if n <= 2:\n"
        "        return False\n"
        "    for i in range(2, n):\n"
        "        if n % i == 0:\n"
        "            return False\n"
        "    return True\n",
        [[17], [18], [2]],
    ),
]


def _compute_expected(solution_code: str, function_name: str, args_list: list) -> list:
    """Runs a correct solution for real to get each test's expected_output.

    Args:
        solution_code: A correct, function-based solution.
        function_name: The function's name.
        args_list: One argument list per test case.

    Returns:
        One expected_output string per entry in args_list.

    Raises:
        RuntimeError: If the solution crashes or times out on any input -
            that means the input choice or the "correct" solution is
            wrong, not that content should ship with a bad expected value.
    """
    tests = [TestCase(args=args, expected_output="") for args in args_list]
    results = run_and_grade_all(solution_code, function_name, tests)
    outputs = []
    for args, result in zip(args_list, results):
        if result.reason.startswith("Your code crashed") or result.reason.startswith("Your code took too long"):
            raise RuntimeError(f"{function_name}{tuple(args)}: reference solution failed: {result.reason}")
        outputs.append(result.actual_output.strip())
    return outputs


def _starter_stub(function_name: str, params_line: str) -> str:
    """Builds a plain TODO stub for a write-from-scratch problem.

    Args:
        function_name: The function's name.
        params_line: The parameter list as it appears in the def line.

    Returns:
        A starter_code stub.
    """
    return f"def {function_name}({params_line}):\n    # TODO: implement this\n    pass\n"


def main():
    """Writes all 24 Loops problem files and reports what it did."""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    # Clear out the old input()-based content before writing the new set.
    for old_file in CONTENT_DIR.glob("*.json"):
        old_file.unlink()

    written = 0

    for problem_id, function_name, prompt, solution, args_list, hint in WRITE_PROBLEMS:
        params_line = solution.split("(", 1)[1].split(")", 1)[0]
        expected_outputs = _compute_expected(solution, function_name, args_list)
        data = {
            "id": problem_id,
            "topic": "loops",
            "title": function_name,
            "prompt": prompt,
            "starter_code": _starter_stub(function_name, params_line),
            "function_name": function_name,
            "tests": [
                {"args": args, "expected_output": expected}
                for args, expected in zip(args_list, expected_outputs)
            ],
            "hint": hint,
        }
        (CONTENT_DIR / f"{problem_id}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        written += 1
        print(f"wrote {problem_id} ({function_name}) - {len(args_list)} test(s)")

    for problem_id, function_name, prompt, solution, buggy_code, args_list in DEBUG_PROBLEMS:
        expected_outputs = _compute_expected(solution, function_name, args_list)

        # Confirm the bug is real: the buggy code must fail at least one test.
        buggy_tests = [
            TestCase(args=args, expected_output=expected)
            for args, expected in zip(args_list, expected_outputs)
        ]
        buggy_results = run_and_grade_all(buggy_code, function_name, buggy_tests)
        if all(r.passed for r in buggy_results):
            raise RuntimeError(f"{problem_id}: buggy starter_code passes every test - not actually buggy!")

        data = {
            "id": problem_id,
            "topic": "loops",
            "title": function_name,
            "prompt": prompt,
            "starter_code": buggy_code,
            "function_name": function_name,
            "tests": [
                {"args": args, "expected_output": expected}
                for args, expected in zip(args_list, expected_outputs)
            ],
            "hint": "",
        }
        (CONTENT_DIR / f"{problem_id}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        written += 1
        print(f"wrote {problem_id} ({function_name}, debug) - confirmed buggy on "
              f"{sum(1 for r in buggy_results if not r.passed)}/{len(buggy_results)} test(s)")

    print(f"\nWrote {written} problem files to {CONTENT_DIR}")


if __name__ == "__main__":
    main()
