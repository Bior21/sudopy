"""One-time authoring script: writes the redesigned Conditionals topic content.

See write_loops_content.py's docstring for the general pattern. Since
Conditionals comes before Loops in the curriculum, every solution here
is deliberately loop-free - no any()/all() over a generator, no
character-by-character scanning - even where a loop would be the
natural real-world tool, matching the vocabulary a student actually has
at this point.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "conditionals_001", "grade_from_score",
        "Given a score, return a letter grade — A for 90+, B for 80+, C for 70+, "
        "D for 60+, and F below that. e.g. score=95 returns 'A'.",
        "def grade_from_score(score):\n"
        "    if score >= 90:\n        return 'A'\n"
        "    elif score >= 80:\n        return 'B'\n"
        "    elif score >= 70:\n        return 'C'\n"
        "    elif score >= 60:\n        return 'D'\n"
        "    else:\n        return 'F'\n",
        [[95], [82], [55]],
        "",
    ),
    (
        "conditionals_002", "classify_bmi",
        "Given a weight in kg and a height in meters, compute the BMI "
        "(weight / height\u00b2) and return its category: 'underweight' below 18.5, "
        "'normal' below 25, 'overweight' below 30, otherwise 'obese'. "
        "e.g. weight_kg=80, height_m=2.0 returns 'normal'.",
        "def classify_bmi(weight_kg, height_m):\n"
        "    bmi = weight_kg / (height_m ** 2)\n"
        "    if bmi < 18.5:\n        return 'underweight'\n"
        "    elif bmi < 25:\n        return 'normal'\n"
        "    elif bmi < 30:\n        return 'overweight'\n"
        "    else:\n        return 'obese'\n",
        [[80, 2.0], [50, 1.7], [100, 1.7]],
        "",
    ),
    (
        "conditionals_003", "shipping_cost",
        "Given a package's weight and the shipping distance, return the cost: $5 if "
        "weight is 5 or under and distance is 100 or under, $15 if only distance is "
        "over 100, $10 if only weight is over 5, otherwise $20. "
        "e.g. weight=3, distance=50 returns 5.",
        "def shipping_cost(weight, distance):\n"
        "    if weight <= 5 and distance <= 100:\n        return 5\n"
        "    elif weight <= 5:\n        return 10\n"
        "    elif distance <= 100:\n        return 15\n"
        "    else:\n        return 20\n",
        [[3, 50], [10, 50], [10, 200]],
        "",
    ),
    (
        "conditionals_004", "is_valid_triangle",
        "Given three side lengths, return whether they can form a triangle (each "
        "side must be shorter than the sum of the other two). "
        "e.g. a=3, b=4, c=5 returns True.",
        "def is_valid_triangle(a, b, c):\n"
        "    return a + b > c and a + c > b and b + c > a\n",
        [[3, 4, 5], [1, 1, 5], [5, 5, 5]],
        "",
    ),
    (
        "conditionals_005", "ticket_price_with_group_discount",
        "Given an age and a group_size, return the ticket price: $5 under 12, $10 "
        "from 12 to 64, $7 for 65+, with a 20% discount if group_size is 5 or more. "
        "e.g. age=30, group_size=2 returns 10.",
        "def ticket_price_with_group_discount(age, group_size):\n"
        "    if age < 12:\n        price = 5\n"
        "    elif age < 65:\n        price = 10\n"
        "    else:\n        price = 7\n"
        "    if group_size >= 5:\n        price = price * 0.8\n"
        "    return price\n",
        [[30, 2], [30, 6], [8, 5]],
        "",
    ),
    (
        "conditionals_006", "overtime_pay",
        "Given hours worked and an hourly_rate, return the pay — the normal rate for "
        "the first 40 hours, and 1.5\u00d7 the rate for anything beyond. "
        "e.g. hours=45, hourly_rate=20 returns 950.0.",
        "def overtime_pay(hours, hourly_rate):\n"
        "    if hours <= 40:\n        return hours * hourly_rate\n"
        "    else:\n"
        "        regular = 40 * hourly_rate\n"
        "        overtime = (hours - 40) * hourly_rate * 1.5\n"
        "        return regular + overtime\n",
        [[35, 20], [45, 20], [40, 15]],
        "",
    ),
    (
        "conditionals_007", "is_leap_year",
        "Given a year, return whether it's a leap year (divisible by 4, except "
        "centuries, which must be divisible by 400). "
        "e.g. year=1900 returns False; year=2000 returns True.",
        "def is_leap_year(year):\n"
        "    if year % 4 != 0:\n        return False\n"
        "    if year % 100 != 0:\n        return True\n"
        "    return year % 400 == 0\n",
        [[2024], [1900], [2000]],
        "",
    ),
    (
        "conditionals_008", "password_strength",
        "Given a password string, return its strength based on length alone: fewer "
        "than 6 characters is 'weak', 6 to 9 is 'medium', 10 or more is 'strong'.",
        "def password_strength(password):\n"
        "    if len(password) < 6:\n        return 'weak'\n"
        "    elif len(password) < 10:\n        return 'medium'\n"
        "    else:\n        return 'strong'\n",
        [["abc"], ["abcdefgh"], ["abcdefghij"]],
        "",
    ),
    (
        "conditionals_009", "tax_owed",
        "Given an income, return the tax owed using tiered brackets: 10% up to "
        "10000, 20% on the amount from 10000 to 40000 (plus 1000), and 30% on "
        "anything above 40000 (plus 7000). e.g. income=25000 returns 4000.0.",
        "def tax_owed(income):\n"
        "    if income <= 10000:\n        return income * 0.1\n"
        "    elif income <= 40000:\n        return 1000 + (income - 10000) * 0.2\n"
        "    else:\n        return 7000 + (income - 40000) * 0.3\n",
        [[5000], [25000], [50000]],
        "",
    ),
    (
        "conditionals_010", "can_checkout",
        "Given a cart_total, whether the customer has a coupon, and the coupon's "
        "minimum spend, return whether checkout can proceed — it's blocked only if "
        "a coupon is claimed but cart_total doesn't meet coupon_minimum. "
        "e.g. cart_total=50, has_coupon=True, coupon_minimum=100 returns False.",
        "def can_checkout(cart_total, has_coupon, coupon_minimum):\n"
        "    return not has_coupon or cart_total >= coupon_minimum\n",
        [[50, False, 100], [150, True, 100], [50, True, 100]],
        "",
    ),
    (
        "conditionals_011", "heat_index_alert",
        "Given a temperature and a humidity percentage, return whether both are "
        "high enough to warrant a heat warning (temp at least 90 and humidity at "
        "least 60). e.g. temp=95, humidity=70 returns True.",
        "def heat_index_alert(temp, humidity):\n"
        "    return temp >= 90 and humidity >= 60\n",
        [[95, 70], [95, 40], [80, 90]],
        "",
    ),
    (
        "conditionals_012", "is_valid_day_for_month",
        "Given a day number and a month number (1-12), return whether day is valid "
        "for that month. Treat February as having 28 days. "
        "e.g. day=31, month=4 returns False (April has 30 days).",
        "def is_valid_day_for_month(day, month):\n"
        "    if day < 1:\n        return False\n"
        "    if month in (1, 3, 5, 7, 8, 10, 12):\n        return day <= 31\n"
        "    elif month in (4, 6, 9, 11):\n        return day <= 30\n"
        "    elif month == 2:\n        return day <= 28\n"
        "    else:\n        return False\n",
        [[31, 1], [31, 4], [30, 2]],
        "",
    ),
    (
        "conditionals_013", "performance_tier",
        "Given a score and three increasing thresholds, return which tier it falls "
        "in: 1 if below threshold1, 2 if below threshold2, 3 if below threshold3, "
        "otherwise 4. e.g. score=80, threshold1=60, threshold2=75, threshold3=90 "
        "returns 3.",
        "def performance_tier(score, threshold1, threshold2, threshold3):\n"
        "    if score >= threshold3:\n        return 4\n"
        "    elif score >= threshold2:\n        return 3\n"
        "    elif score >= threshold1:\n        return 2\n"
        "    else:\n        return 1\n",
        [[95, 60, 75, 90], [80, 60, 75, 90], [50, 60, 75, 90]],
        "",
    ),
    (
        "conditionals_014", "is_valid_username",
        "Given a username, return whether it's 3 to 16 characters long and contains "
        "no spaces. e.g. username='ab' returns False.",
        "def is_valid_username(username):\n"
        "    return 3 <= len(username) <= 16 and ' ' not in username\n",
        [["ab"], ["validname"], ["has space"]],
        "",
    ),
    (
        "conditionals_015", "late_fee",
        "Given how many days a payment is late, return the fee: 0 if not late, $5 "
        "up to a week late, $15 up to a month late, otherwise $30. "
        "e.g. days_late=45 returns 30.",
        "def late_fee(days_late):\n"
        "    if days_late <= 0:\n        return 0\n"
        "    elif days_late <= 7:\n        return 5\n"
        "    elif days_late <= 30:\n        return 15\n"
        "    else:\n        return 30\n",
        [[0], [5], [45]],
        "",
    ),
    (
        "conditionals_016", "can_move_elevator",
        "Given the elevator's current_floor, a requested_floor, and the building's "
        "max_floor, return whether the request is valid — in range and different "
        "from the current floor. e.g. current_floor=3, requested_floor=3, "
        "max_floor=10 returns False.",
        "def can_move_elevator(current_floor, requested_floor, max_floor):\n"
        "    return 1 <= requested_floor <= max_floor and requested_floor != current_floor\n",
        [[3, 5, 10], [3, 3, 10], [3, 15, 10]],
        "",
    ),
    (
        "conditionals_017", "discount_tier",
        "Given a total_spent amount, return the discount percentage earned: 20% at "
        "500+, 10% at 200+, 5% at 50+, otherwise 0. e.g. total_spent=100 returns 5.",
        "def discount_tier(total_spent):\n"
        "    if total_spent >= 500:\n        return 20\n"
        "    elif total_spent >= 200:\n        return 10\n"
        "    elif total_spent >= 50:\n        return 5\n"
        "    else:\n        return 0\n",
        [[600], [100], [10]],
        "",
    ),
    (
        "conditionals_018", "is_business_day",
        "Given a day name, return whether it's a business day (not Saturday or "
        "Sunday). e.g. day_name='Saturday' returns False.",
        "def is_business_day(day_name):\n"
        "    return day_name not in ('Saturday', 'Sunday')\n",
        [["Monday"], ["Saturday"], ["Friday"]],
        "",
    ),
    (
        "conditionals_019", "compare_three_way",
        "Given two numbers a and b, return -1 if a is smaller, 1 if a is larger, or "
        "0 if they're equal. e.g. a=3, b=5 returns -1.",
        "def compare_three_way(a, b):\n"
        "    if a < b:\n        return -1\n"
        "    elif a > b:\n        return 1\n"
        "    else:\n        return 0\n",
        [[3, 5], [5, 3], [4, 4]],
        "",
    ),
    (
        "conditionals_020", "fizz_or_buzz",
        "Given an int n, return 'fizzbuzz' if it's divisible by both 3 and 5, "
        "'fizz' if just by 3, 'buzz' if just by 5, otherwise str(n). "
        "e.g. n=15 returns 'fizzbuzz'.",
        "def fizz_or_buzz(n):\n"
        "    if n % 15 == 0:\n        return 'fizzbuzz'\n"
        "    elif n % 3 == 0:\n        return 'fizz'\n"
        "    elif n % 5 == 0:\n        return 'buzz'\n"
        "    else:\n        return str(n)\n",
        [[15], [9], [7]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "conditionals_debug_001", "grade_from_score",
        "Given a score, this function is supposed to return a letter grade (A for "
        "90+, B for 80+, C for 70+, D for 60+, F below) — but it has a bug. "
        "Find it and fix it.",
        "def grade_from_score(score):\n"
        "    if score >= 90:\n        return 'A'\n"
        "    elif score >= 80:\n        return 'B'\n"
        "    elif score >= 70:\n        return 'C'\n"
        "    elif score >= 60:\n        return 'D'\n"
        "    else:\n        return 'F'\n",
        "def grade_from_score(score):\n"
        "    if score > 90:\n        return 'A'\n"
        "    elif score >= 80:\n        return 'B'\n"
        "    elif score >= 70:\n        return 'C'\n"
        "    elif score >= 60:\n        return 'D'\n"
        "    else:\n        return 'F'\n",
        [[95], [90], [55]],
    ),
    (
        "conditionals_debug_002", "is_leap_year",
        "Given a year, this function is supposed to return whether it's a leap "
        "year — but it has a bug. Find it and fix it.",
        "def is_leap_year(year):\n"
        "    if year % 4 != 0:\n        return False\n"
        "    if year % 100 != 0:\n        return True\n"
        "    return year % 400 == 0\n",
        "def is_leap_year(year):\n"
        "    return year % 4 == 0\n",
        [[2024], [1900], [2000]],
    ),
    (
        "conditionals_debug_003", "fizz_or_buzz",
        "Given an int n, this function is supposed to return 'fizzbuzz', 'fizz', "
        "'buzz', or str(n) depending on divisibility by 3 and 5 — but it has a bug. "
        "Find it and fix it.",
        "def fizz_or_buzz(n):\n"
        "    if n % 15 == 0:\n        return 'fizzbuzz'\n"
        "    elif n % 3 == 0:\n        return 'fizz'\n"
        "    elif n % 5 == 0:\n        return 'buzz'\n"
        "    else:\n        return str(n)\n",
        "def fizz_or_buzz(n):\n"
        "    if n % 5 == 0:\n        return 'buzz'\n"
        "    elif n % 3 == 0:\n        return 'fizz'\n"
        "    else:\n        return str(n)\n",
        [[15], [9], [7]],
    ),
    (
        "conditionals_debug_004", "compare_three_way",
        "Given two numbers a and b, this function is supposed to return -1, 0, or "
        "1 depending on how they compare — but it has a bug. Find it and fix it.",
        "def compare_three_way(a, b):\n"
        "    if a < b:\n        return -1\n"
        "    elif a > b:\n        return 1\n"
        "    else:\n        return 0\n",
        "def compare_three_way(a, b):\n"
        "    if a < b:\n        return 1\n"
        "    elif a > b:\n        return -1\n"
        "    else:\n        return 0\n",
        [[3, 5], [5, 3], [4, 4]],
    ),
]


def main():
    """Writes all 24 Conditionals problem files and reports what it did."""
    written = write_topic("conditionals", "04_conditionals", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
