"""One-time authoring script: writes the redesigned Operators topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "operators_001", "total_with_compound_discount",
        "Given a price and two discount percentages, apply them one after another "
        "(discount1 first, then discount2 on the reduced price) and return the final "
        "price. e.g. price=100, discount1=20, discount2=10 returns 72.0.",
        "def total_with_compound_discount(price, discount1, discount2):\n"
        "    after_first = price - price * discount1 / 100\n"
        "    after_second = after_first - after_first * discount2 / 100\n"
        "    return after_second\n",
        [[100, 20, 10], [200, 50, 50], [50, 0, 0]],
        "",
    ),
    (
        "operators_002", "is_between_exclusive",
        "Given a number n and a low/high range, return whether n is strictly between "
        "low and high (not equal to either). e.g. n=5, low=1, high=10 returns True.",
        "def is_between_exclusive(n, low, high):\n    return low < n < high\n",
        [[5, 1, 10], [1, 1, 10], [10, 1, 10]],
        "",
    ),
    (
        "operators_003", "items_left_over",
        "Given a total number of items and a group_size, return how many are left over "
        "after making as many full groups as possible. e.g. total=17, group_size=5 "
        "returns 2.",
        "def items_left_over(total, group_size):\n    return total % group_size\n",
        [[17, 5], [20, 4], [7, 3]],
        "",
    ),
    (
        "operators_004", "pages_needed",
        "Given a number of items and how many fit per page, return how many pages it "
        "takes, rounding up. e.g. items=23, items_per_page=10 returns 3.",
        "def pages_needed(items, items_per_page):\n"
        "    return (items + items_per_page - 1) // items_per_page\n",
        [[23, 10], [20, 10], [1, 10]],
        "There's a way to round up using only integer division — add items_per_page - 1 first.",
    ),
    (
        "operators_005", "is_strictly_increasing",
        "Given three numbers a, b, c, return whether each is strictly greater than the "
        "one before it. e.g. a=1, b=2, c=3 returns True.",
        "def is_strictly_increasing(a, b, c):\n    return a < b < c\n",
        [[1, 2, 3], [3, 2, 1], [1, 1, 2]],
        "",
    ),
    (
        "operators_006", "same_sign",
        "Given two numbers a and b, return whether they're both positive or both "
        "negative. e.g. a=5, b=3 returns True; a=5, b=-3 returns False.",
        "def same_sign(a, b):\n    return (a > 0 and b > 0) or (a < 0 and b < 0)\n",
        [[5, 3], [-5, -3], [5, -3]],
        "",
    ),
    (
        "operators_007", "weighted_score",
        "Given two scores and a weight for each (weights that add up to 1), return the "
        "weighted combination. e.g. score1=80, weight1=0.6, score2=90, weight2=0.4 "
        "returns 84.0.",
        "def weighted_score(score1, weight1, score2, weight2):\n"
        "    return score1 * weight1 + score2 * weight2\n",
        [[80, 0.6, 90, 0.4], [100, 0.5, 50, 0.5], [70, 1, 0, 0]],
        "",
    ),
    (
        "operators_008", "distance_squared",
        "Given the coordinates of two points, return the squared distance between them "
        "(skip the square root). e.g. x1=0, y1=0, x2=3, y2=4 returns 25.",
        "def distance_squared(x1, y1, x2, y2):\n"
        "    return (x2 - x1) ** 2 + (y2 - y1) ** 2\n",
        [[0, 0, 3, 4], [1, 1, 1, 1], [0, 0, 1, 1]],
        "",
    ),
    (
        "operators_009", "is_close_enough",
        "Given two numbers a and b and a tolerance, return whether they differ by no "
        "more than tolerance. e.g. a=5, b=5.05, tolerance=0.1 returns True.",
        "def is_close_enough(a, b, tolerance):\n    return abs(a - b) <= tolerance\n",
        [[5, 5.05, 0.1], [5, 5.2, 0.1], [5, 6, 1]],
        "",
    ),
    (
        "operators_010", "total_area_two_rectangles",
        "Given the width and height of two rectangles, return their combined area. "
        "e.g. w1=3, h1=4, w2=5, h2=6 returns 42.",
        "def total_area_two_rectangles(w1, h1, w2, h2):\n"
        "    return w1 * h1 + w2 * h2\n",
        [[3, 4, 5, 6], [1, 1, 1, 1], [10, 2, 0, 5]],
        "",
    ),
    (
        "operators_011", "percentage_change",
        "Given an old_value and a new_value, return the percent change from old to "
        "new. e.g. old_value=50, new_value=75 returns 50.0.",
        "def percentage_change(old_value, new_value):\n"
        "    return (new_value - old_value) / old_value * 100\n",
        [[50, 75], [100, 90], [40, 40]],
        "",
    ),
    (
        "operators_012", "is_multiple_of_either",
        "Given a number n and two factors a and b, return whether n is a multiple of "
        "a or of b. e.g. n=15, a=3, b=5 returns True.",
        "def is_multiple_of_either(n, a, b):\n    return n % a == 0 or n % b == 0\n",
        [[15, 3, 5], [7, 3, 5], [10, 3, 5]],
        "",
    ),
    (
        "operators_013", "last_two_digits",
        "Given an int n, return its last two digits as a number. "
        "e.g. n=12345 returns 45.",
        "def last_two_digits(n):\n    return n % 100\n",
        [[12345], [7], [100]],
        "",
    ),
    (
        "operators_014", "round_down_to_nearest",
        "Given a number n and a multiple, return n rounded down to the nearest "
        "multiple. e.g. n=47, multiple=10 returns 40.",
        "def round_down_to_nearest(n, multiple):\n"
        "    return (n // multiple) * multiple\n",
        [[47, 10], [99, 5], [12, 4]],
        "",
    ),
    (
        "operators_015", "round_up_to_nearest",
        "Given a number n and a multiple, return n rounded up to the nearest multiple. "
        "e.g. n=47, multiple=10 returns 50.",
        "def round_up_to_nearest(n, multiple):\n"
        "    return ((n + multiple - 1) // multiple) * multiple\n",
        [[47, 10], [95, 5], [41, 4]],
        "",
    ),
    (
        "operators_016", "exponential_growth",
        "Given an initial value, a growth rate (as a fraction), and a number of "
        "periods, return the value after growing at that rate for that many periods. "
        "e.g. initial=100, rate=0.5, periods=2 returns 225.0.",
        "def exponential_growth(initial, rate, periods):\n"
        "    return initial * (1 + rate) ** periods\n",
        [[100, 0.5, 2], [80, 1, 3], [50, 0, 5]],
        "",
    ),
    (
        "operators_017", "should_send_alert",
        "Given two booleans is_critical and is_acknowledged, return whether an alert "
        "should fire — only when it's critical and hasn't been acknowledged yet. "
        "e.g. is_critical=True, is_acknowledged=False returns True.",
        "def should_send_alert(is_critical, is_acknowledged):\n"
        "    return is_critical and not is_acknowledged\n",
        [[True, False], [True, True], [False, False]],
        "",
    ),
    (
        "operators_018", "harmonic_mean_of_two",
        "Given two positive numbers a and b, return their harmonic mean "
        "(2ab / (a+b)). e.g. a=4, b=4 returns 4.0.",
        "def harmonic_mean_of_two(a, b):\n    return 2 * a * b / (a + b)\n",
        [[4, 4], [2, 8], [10, 10]],
        "",
    ),
    (
        "operators_019", "body_mass_index",
        "Given a weight in kg and a height in meters, return the BMI (weight divided "
        "by height squared). e.g. weight_kg=80, height_m=2.0 returns 20.0.",
        "def body_mass_index(weight_kg, height_m):\n"
        "    return weight_kg / (height_m ** 2)\n",
        [[70, 1.75], [80, 2.0], [50, 1.0]],
        "",
    ),
    (
        "operators_020", "is_right_triangle",
        "Given three side lengths a, b, c where c is the longest, return whether they "
        "form a right triangle. e.g. a=3, b=4, c=5 returns True.",
        "def is_right_triangle(a, b, c):\n    return a ** 2 + b ** 2 == c ** 2\n",
        [[3, 4, 5], [5, 6, 7], [6, 8, 10]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "operators_debug_001", "percentage_change",
        "Given old_value and new_value, this function is supposed to return the "
        "percent change from old to new — but it has a bug. Find it and fix it.",
        "def percentage_change(old_value, new_value):\n"
        "    return (new_value - old_value) / old_value * 100\n",
        "def percentage_change(old_value, new_value):\n"
        "    return (new_value - old_value) / new_value * 100\n",
        [[50, 75], [100, 90], [20, 80]],
    ),
    (
        "operators_debug_002", "is_close_enough",
        "Given a, b, and tolerance, this function is supposed to return whether a and "
        "b differ by no more than tolerance — but it has a bug. Find it and fix it.",
        "def is_close_enough(a, b, tolerance):\n    return abs(a - b) <= tolerance\n",
        "def is_close_enough(a, b, tolerance):\n    return abs(a - b) < tolerance\n",
        [[5, 6, 1], [5, 5.05, 0.1], [5, 7, 1]],
    ),
    (
        "operators_debug_003", "round_down_to_nearest",
        "Given n and multiple, this function is supposed to return n rounded down to "
        "the nearest multiple — but it has a bug. Find it and fix it.",
        "def round_down_to_nearest(n, multiple):\n"
        "    return (n // multiple) * multiple\n",
        "def round_down_to_nearest(n, multiple):\n"
        "    return (n // multiple + 1) * multiple\n",
        [[47, 10], [99, 5], [12, 4]],
    ),
    (
        "operators_debug_004", "is_right_triangle",
        "Given three side lengths a, b, c where c is the longest, this function is "
        "supposed to return whether they form a right triangle — but it has a bug. "
        "Find it and fix it.",
        "def is_right_triangle(a, b, c):\n    return a ** 2 + b ** 2 == c ** 2\n",
        "def is_right_triangle(a, b, c):\n    return a ** 2 + c ** 2 == b ** 2\n",
        [[3, 4, 5], [5, 6, 7], [6, 8, 10]],
    ),
]


def main():
    """Writes all 24 Operators problem files and reports what it did."""
    written = write_topic("operators", "02_operators", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
