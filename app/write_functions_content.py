"""One-time authoring script: writes the redesigned Functions topic content.

See write_loops_content.py's docstring for the general pattern. Many
solutions here define a helper function before the target one - that's
deliberate: content_authoring.starter_stub() keeps everything before the
target function's own def line verbatim, so the helper ships already
working in starter_code and only the target function is a TODO stub.
No recursion anywhere - see the curriculum plan for why.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "functions_001", "lucky_number",
        "Return a fixed lucky number — no parameters needed at all. "
        "e.g. lucky_number() returns 7.",
        "def lucky_number():\n    return 7\n",
        [[]],
        "",
    ),
    (
        "functions_002", "greet",
        "Given a name and an optional greeting (default 'Hello'), return them "
        "combined as '{greeting}, {name}!'. e.g. greet('Ana') returns 'Hello, Ana!'; "
        "greet('Sam', 'Hi') returns 'Hi, Sam!'.",
        "def greet(name, greeting='Hello'):\n"
        "    return f'{greeting}, {name}!'\n",
        [["Ana"], ["Sam", "Hi"]],
        "",
    ),
    (
        "functions_003", "describe_person",
        "Given a name, an age, and an optional city (default 'Unknown'), return a "
        "sentence describing them. e.g. describe_person('Ana', 20) returns "
        "'Ana is 20 years old and lives in Unknown.'.",
        "def describe_person(name, age, city='Unknown'):\n"
        "    return f'{name} is {age} years old and lives in {city}.'\n",
        [["Ana", 20], ["Sam", 30, "Austin"]],
        "",
    ),
    (
        "functions_004", "announce_winner",
        "Given a name, print '{name} wins!' — this one doesn't return anything, it "
        "just prints directly.",
        "def announce_winner(name):\n    print(f'{name} wins!')\n",
        [["Ana"], ["Sam"]],
        "",
    ),
    (
        "functions_005", "safe_divide",
        "Given a and b, return a divided by b — or an optional default (0 if not "
        "given) if b is zero, instead of crashing. e.g. safe_divide(10, 0) returns 0.",
        "def safe_divide(a, b, default=0):\n"
        "    if b == 0:\n        return default\n"
        "    return a / b\n",
        [[10, 2], [10, 0], [10, 0, -1]],
        "",
    ),
    (
        "functions_006", "describe_rectangle",
        "Given a width and height, return both the area and the perimeter, as a "
        "tuple. e.g. width=3, height=4 returns (12, 14).",
        "def describe_rectangle(width, height):\n"
        "    area = width * height\n"
        "    perimeter = 2 * (width + height)\n"
        "    return area, perimeter\n",
        [[3, 4], [5, 5]],
        "",
    ),
    (
        "functions_007", "min_and_max",
        "Given a list of numbers, return the smallest and largest, as a tuple. "
        "e.g. nums=[3, 1, 4, 1, 5] returns (1, 5).",
        "def min_and_max(nums):\n    return min(nums), max(nums)\n",
        [[[3, 1, 4, 1, 5]], [[7]]],
        "",
    ),
    (
        "functions_008", "divide_with_remainder",
        "Given a and b, return the quotient and remainder of a divided by b, as a "
        "tuple. e.g. a=17, b=5 returns (3, 2).",
        "def divide_with_remainder(a, b):\n    return a // b, a % b\n",
        [[17, 5], [20, 4]],
        "",
    ),
    (
        "functions_009", "total_and_average",
        "Given a list of numbers, return both the sum and the average, as a tuple. "
        "e.g. nums=[10, 20, 30] returns (60, 20.0).",
        "def total_and_average(nums):\n"
        "    total = sum(nums)\n"
        "    average = total / len(nums)\n"
        "    return total, average\n",
        [[[10, 20, 30]], [[5, 5]]],
        "",
    ),
    (
        "functions_010", "classify_and_count",
        "Given a list of numbers, return how many are positive, negative, and zero, "
        "as a 3-tuple. e.g. nums=[1, -2, 3, 0, -5] returns (2, 2, 1).",
        "def classify_and_count(nums):\n"
        "    positives = 0\n    negatives = 0\n    zeros = 0\n"
        "    for n in nums:\n"
        "        if n > 0:\n            positives += 1\n"
        "        elif n < 0:\n            negatives += 1\n"
        "        else:\n            zeros += 1\n"
        "    return positives, negatives, zeros\n",
        [[[1, -2, 3, 0, -5]], [[1, 2, 3]]],
        "",
    ),
    (
        "functions_011", "count_evens",
        "A working is_even(n) is already defined above. Given a list of numbers, "
        "use it to count how many are even. e.g. nums=[1, 2, 3, 4, 5, 6] returns 3.",
        "def is_even(n):\n    return n % 2 == 0\n\n\n"
        "def count_evens(nums):\n"
        "    count = 0\n"
        "    for n in nums:\n"
        "        if is_even(n):\n            count += 1\n"
        "    return count\n",
        [[[1, 2, 3, 4, 5, 6]], [[1, 3, 5]]],
        "",
    ),
    (
        "functions_012", "weather_report",
        "A working celsius_to_fahrenheit(c) is already defined above. Given a "
        "temperature in celsius, use it to return a one-line report. "
        "e.g. c=20 returns \"It's 68.0 degrees Fahrenheit.\".",
        "def celsius_to_fahrenheit(c):\n    return c * 9 / 5 + 32\n\n\n"
        "def weather_report(c):\n"
        "    f = celsius_to_fahrenheit(c)\n"
        "    return f\"It's {f} degrees Fahrenheit.\"\n",
        [[20], [0]],
        "",
    ),
    (
        "functions_013", "sum_of_squares",
        "A working square(n) is already defined above. Given a list of numbers, "
        "use it to return the sum of their squares. e.g. nums=[1, 2, 3] returns 14.",
        "def square(n):\n    return n * n\n\n\n"
        "def sum_of_squares(nums):\n"
        "    total = 0\n"
        "    for n in nums:\n        total += square(n)\n"
        "    return total\n",
        [[[1, 2, 3]], [[2, 4]]],
        "",
    ),
    (
        "functions_014", "total_area_of_squares",
        "A working area_of_square(side) is already defined above. Given a list of "
        "side lengths, use it to return the total area. "
        "e.g. sides=[2, 3, 4] returns 29.",
        "def area_of_square(side):\n    return side * side\n\n\n"
        "def total_area_of_squares(sides):\n"
        "    total = 0\n"
        "    for side in sides:\n        total += area_of_square(side)\n"
        "    return total\n",
        [[[2, 3, 4]], [[5]]],
        "",
    ),
    (
        "functions_015", "all_passwords_valid",
        "A working is_valid_password_length(pw) is already defined above. Given a "
        "list of passwords, use it to return whether every one of them is valid. "
        "e.g. passwords=['longenough1', 'longenough2'] returns True.",
        "def is_valid_password_length(pw):\n    return len(pw) >= 8\n\n\n"
        "def all_passwords_valid(passwords):\n"
        "    for pw in passwords:\n"
        "        if not is_valid_password_length(pw):\n            return False\n"
        "    return True\n",
        [[["longenough1", "longenough2"]], [["short", "longenough1"]]],
        "",
    ),
    (
        "functions_016", "fahrenheit_report_list",
        "A working celsius_to_fahrenheit(c) is already defined above. Given a list "
        "of celsius temperatures, use it to return a list of their Fahrenheit "
        "equivalents. e.g. celsius_list=[0, 20, 100] returns [32.0, 68.0, 212.0].",
        "def celsius_to_fahrenheit(c):\n    return c * 9 / 5 + 32\n\n\n"
        "def fahrenheit_report_list(celsius_list):\n"
        "    result = []\n"
        "    for c in celsius_list:\n        result.append(celsius_to_fahrenheit(c))\n"
        "    return result\n",
        [[[0, 20, 100]]],
        "",
    ),
    (
        "functions_017", "count_passing_scores",
        "A working is_passing(score) is already defined above. Given a list of "
        "scores, use it to count how many pass. "
        "e.g. scores=[85, 45, 60, 90, 30] returns 3.",
        "def is_passing(score):\n    return score >= 60\n\n\n"
        "def count_passing_scores(scores):\n"
        "    count = 0\n"
        "    for score in scores:\n"
        "        if is_passing(score):\n            count += 1\n"
        "    return count\n",
        [[[85, 45, 60, 90, 30]], [[50, 55]]],
        "",
    ),
    (
        "functions_018", "total_cost_for_order",
        "A working total_cost(price, quantity) is already defined above. Given "
        "parallel lists of prices and quantities, use it to return the total cost "
        "of the whole order. e.g. prices=[10, 20], quantities=[2, 3] returns 80.",
        "def total_cost(price, quantity):\n    return price * quantity\n\n\n"
        "def total_cost_for_order(prices, quantities):\n"
        "    total = 0\n"
        "    for i in range(len(prices)):\n"
        "        total += total_cost(prices[i], quantities[i])\n"
        "    return total\n",
        [[[10, 20], [2, 3]], [[5], [4]]],
        "",
    ),
    (
        "functions_019", "apply_discount_twice",
        "A working discounted_price(price, discount_percent) is already defined "
        "above. Given a price and a discount_percent, use it twice in a row and "
        "return the final price. e.g. price=100, discount_percent=10 returns 81.0.",
        "def discounted_price(price, discount_percent):\n"
        "    return price - price * discount_percent / 100\n\n\n"
        "def apply_discount_twice(price, discount_percent):\n"
        "    once = discounted_price(price, discount_percent)\n"
        "    twice = discounted_price(once, discount_percent)\n"
        "    return twice\n",
        [[100, 10], [200, 50]],
        "",
    ),
    (
        "functions_020", "format_receipt",
        "A working total_cost(price, quantity) is already defined above. Given an "
        "item name, price, and quantity, use it plus string formatting to return a "
        "receipt line like '3x apple: $6'.",
        "def total_cost(price, quantity):\n    return price * quantity\n\n\n"
        "def format_receipt(item, price, quantity):\n"
        "    cost = total_cost(price, quantity)\n"
        "    return f'{quantity}x {item}: ${cost}'\n",
        [["apple", 2, 3], ["book", 15, 1]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "functions_debug_001", "safe_divide",
        "Given a, b, and an optional default, this function is supposed to return "
        "a divided by b, or default if b is zero — but it has a bug. "
        "Find it and fix it.",
        "def safe_divide(a, b, default=0):\n"
        "    if b == 0:\n        return default\n"
        "    return a / b\n",
        "def safe_divide(a, b, default=0):\n"
        "    if b is None:\n        return default\n"
        "    return a / b\n",
        [[10, 2], [10, 0], [10, 0, -1]],
    ),
    (
        "functions_debug_002", "describe_rectangle",
        "Given width and height, this function is supposed to return "
        "(area, perimeter) as a tuple — but it has a bug. Find it and fix it.",
        "def describe_rectangle(width, height):\n"
        "    area = width * height\n"
        "    perimeter = 2 * (width + height)\n"
        "    return area, perimeter\n",
        "def describe_rectangle(width, height):\n"
        "    area = width * height\n"
        "    perimeter = 2 * (width + height)\n"
        "    return perimeter, area\n",
        [[3, 4], [5, 5]],
    ),
    (
        "functions_debug_003", "count_evens",
        "A helper is_even(n) is defined above. This function is supposed to use "
        "it to count the even numbers in nums — but it has a bug. "
        "Find it and fix it.",
        "def is_even(n):\n    return n % 2 == 0\n\n\n"
        "def count_evens(nums):\n"
        "    count = 0\n"
        "    for n in nums:\n"
        "        if is_even(n):\n            count += 1\n"
        "    return count\n",
        "def is_even(n):\n    return n % 2 == 0\n\n\n"
        "def count_evens(nums):\n"
        "    count = 0\n"
        "    for n in nums:\n"
        "        if is_even():\n            count += 1\n"
        "    return count\n",
        [[[1, 2, 3, 4, 5, 6]], [[1, 3, 5]]],
    ),
    (
        "functions_debug_004", "total_and_average",
        "Given a list of numbers, this function is supposed to return both the "
        "sum and the average — but it has a bug. Find it and fix it.",
        "def total_and_average(nums):\n"
        "    total = sum(nums)\n"
        "    average = total / len(nums)\n"
        "    return total, average\n",
        "def total_and_average(nums):\n"
        "    total = sum(nums)\n"
        "    average = total / 3\n"
        "    return total, average\n",
        [[[10, 20]], [[5, 5, 5, 5]], [[10, 20, 30]]],
    ),
]


def main():
    """Writes all 24 Functions problem files and reports what it did."""
    written = write_topic("functions", "06_functions", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
