"""One-time authoring script: writes the redesigned Variables topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "variables_001", "total_after_tax",
        "Given a price and a tax_rate (as a fraction, e.g. 0.08 for 8%), return the "
        "total price including tax. e.g. price=100, tax_rate=0.08 returns 108.0.",
        "def total_after_tax(price, tax_rate):\n    return price + price * tax_rate\n",
        [[100, 0.08], [40, 0.25], [200, 0.05]],
        "",
    ),
    (
        "variables_002", "temperature_swing",
        "Given the temperature in the morning and in the evening, return how much it "
        "changed (can be negative). e.g. morning_temp=60, evening_temp=75 returns 15.",
        "def temperature_swing(morning_temp, evening_temp):\n    return evening_temp - morning_temp\n",
        [[60, 75], [80, 68], [50, 50]],
        "",
    ),
    (
        "variables_003", "time_to_seconds",
        "Given a number of hours and minutes, return the total number of seconds. "
        "e.g. hours=1, minutes=30 returns 5400.",
        "def time_to_seconds(hours, minutes):\n    return hours * 3600 + minutes * 60\n",
        [[1, 30], [0, 5], [2, 0]],
        "",
    ),
    (
        "variables_004", "split_the_bill_with_tip",
        "Given a bill total, a number of people, and a tip_rate (as a fraction), return "
        "each person's share, tip included. e.g. total=100, people=4, tip_rate=0.2 "
        "returns 30.0.",
        "def split_the_bill_with_tip(total, people, tip_rate):\n"
        "    return (total + total * tip_rate) / people\n",
        [[100, 4, 0.2], [50, 2, 0.1], [90, 3, 0.0]],
        "",
    ),
    (
        "variables_005", "age_gap",
        "Given two ages, return the difference between them, regardless of which one "
        "is older. e.g. age1=15, age2=22 returns 7.",
        "def age_gap(age1, age2):\n    return abs(age1 - age2)\n",
        [[15, 22], [30, 12], [20, 20]],
        "",
    ),
    (
        "variables_006", "exceeds_when_converted",
        "Given a temperature in celsius and a fahrenheit_limit, convert celsius to "
        "Fahrenheit and return whether it exceeds fahrenheit_limit. e.g. celsius=30, "
        "fahrenheit_limit=80 returns True (30°C is 86°F).",
        "def exceeds_when_converted(celsius, fahrenheit_limit):\n"
        "    fahrenheit = celsius * 9 / 5 + 32\n"
        "    return fahrenheit > fahrenheit_limit\n",
        [[30, 80], [10, 100], [0, 31]],
        "Fahrenheit = Celsius × 9/5 + 32.",
    ),
    (
        "variables_007", "remaining_after_purchase",
        "Given a balance, a price, and a quantity, return what's left of balance after "
        "buying quantity items at price each. e.g. balance=100, price=15, quantity=3 "
        "returns 55.",
        "def remaining_after_purchase(balance, price, quantity):\n"
        "    return balance - price * quantity\n",
        [[100, 15, 3], [50, 10, 6], [200, 25, 4]],
        "",
    ),
    (
        "variables_008", "paces_to_meters",
        "Given a number of paces and the length of each pace in meters, return the "
        "total distance covered. e.g. paces=100, pace_length=0.75 returns 75.0.",
        "def paces_to_meters(paces, pace_length):\n    return paces * pace_length\n",
        [[100, 0.75], [50, 1.2], [10, 2.0]],
        "",
    ),
    (
        "variables_009", "is_within_one_year",
        "Given two ages, return whether they're at most a year apart. "
        "e.g. age1=15, age2=16 returns True.",
        "def is_within_one_year(age1, age2):\n    return abs(age1 - age2) <= 1\n",
        [[15, 16], [15, 20], [10, 10]],
        "",
    ),
    (
        "variables_010", "formatted_id",
        "Given a first name, a last name, and an id_number, return them formatted as "
        "'Last, First (#id_number)'. e.g. first='Ana', last='Lopez', id_number=42 "
        "returns 'Lopez, Ana (#42)'.",
        "def formatted_id(first, last, id_number):\n"
        "    return f'{last}, {first} (#{id_number})'\n",
        [["Ana", "Lopez", 42], ["Sam", "Diaz", 7], ["Zoe", "Ali", 100]],
        "",
    ),
    (
        "variables_011", "discounted_price",
        "Given a price and a discount_percent, return the price after taking off that "
        "percentage. e.g. price=200, discount_percent=25 returns 150.0.",
        "def discounted_price(price, discount_percent):\n"
        "    return price - price * discount_percent / 100\n",
        [[200, 25], [80, 10], [50, 0]],
        "",
    ),
    (
        "variables_012", "speed_from_distance_time",
        "Given a distance and a time, return the speed implied by covering that "
        "distance in that time. e.g. distance=100, time=4 returns 25.0.",
        "def speed_from_distance_time(distance, time):\n    return distance / time\n",
        [[100, 4], [60, 1.5], [10, 2]],
        "",
    ),
    (
        "variables_013", "total_distance_two_legs",
        "Given the speed and time for two separate legs of a trip, return the total "
        "distance covered. e.g. speed1=60, time1=2, speed2=80, time2=1 returns 200.",
        "def total_distance_two_legs(speed1, time1, speed2, time2):\n"
        "    return speed1 * time1 + speed2 * time2\n",
        [[60, 2, 80, 1], [50, 1, 50, 1], [30, 3, 0, 5]],
        "",
    ),
    (
        "variables_014", "profit",
        "Given a revenue and a cost, return the profit (can be negative if cost "
        "exceeds revenue). e.g. revenue=500, cost=300 returns 200.",
        "def profit(revenue, cost):\n    return revenue - cost\n",
        [[500, 300], [200, 350], [100, 100]],
        "",
    ),
    (
        "variables_015", "year_someone_turns_age",
        "Given a birth_year and a target_age, return the year someone born in "
        "birth_year turns target_age. e.g. birth_year=2010, target_age=18 returns 2028.",
        "def year_someone_turns_age(birth_year, target_age):\n"
        "    return birth_year + target_age\n",
        [[2010, 18], [2000, 30], [2015, 21]],
        "",
    ),
    (
        "variables_016", "flag_to_bit",
        "Given a boolean is_active, return it converted to an integer — True "
        "becomes 1, False becomes 0. e.g. is_active=True returns 1.",
        "def flag_to_bit(is_active):\n    return int(is_active)\n",
        [[True], [False]],
        "",
    ),
    (
        "variables_017", "average_speed",
        "Given a distance covered over a trip split into two timed parts, return the "
        "average speed. e.g. distance=100, time1=2, time2=3 returns 20.0.",
        "def average_speed(distance, time1, time2):\n"
        "    return distance / (time1 + time2)\n",
        [[100, 2, 3], [90, 1, 2], [50, 5, 5]],
        "",
    ),
    (
        "variables_018", "can_afford",
        "Given a balance and a price, return whether balance covers price. "
        "e.g. balance=100, price=80 returns True.",
        "def can_afford(balance, price):\n    return balance >= price\n",
        [[100, 80], [50, 80], [80, 80]],
        "",
    ),
    (
        "variables_019", "total_inches",
        "Given a length in feet and inches, return the total length in inches. "
        "e.g. feet=5, inches=6 returns 66.",
        "def total_inches(feet, inches):\n    return feet * 12 + inches\n",
        [[5, 6], [2, 11], [0, 5]],
        "",
    ),
    (
        "variables_020", "net_change",
        "Given a start_value and an end_value, return how much it changed. "
        "e.g. start_value=50, end_value=75 returns 25.",
        "def net_change(start_value, end_value):\n    return end_value - start_value\n",
        [[50, 75], [100, 60], [10, 10]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "variables_debug_001", "speed_from_distance_time",
        "Given distance and time, this function is supposed to return the speed "
        "implied by covering distance in time — but it has a bug. Find it and fix it.",
        "def speed_from_distance_time(distance, time):\n    return distance / time\n",
        "def speed_from_distance_time(distance, time):\n    return time / distance\n",
        [[100, 4], [60, 1.5], [10, 2]],
    ),
    (
        "variables_debug_002", "discounted_price",
        "Given price and discount_percent, this function is supposed to return the "
        "price after taking off that percentage — but it has a bug. Find it and fix it.",
        "def discounted_price(price, discount_percent):\n"
        "    return price - price * discount_percent / 100\n",
        "def discounted_price(price, discount_percent):\n"
        "    return price + price * discount_percent / 100\n",
        [[200, 25], [80, 10], [50, 0]],
    ),
    (
        "variables_debug_003", "formatted_id",
        "Given first, last, and id_number, this function is supposed to return them "
        "formatted as 'Last, First (#id_number)' — but it has a bug. Find it and fix it.",
        "def formatted_id(first, last, id_number):\n"
        "    return f'{last}, {first} (#{id_number})'\n",
        "def formatted_id(first, last, id_number):\n"
        "    return f'{last},{first} (#{id_number})'\n",
        [["Ana", "Lopez", 42], ["Sam", "Diaz", 7], ["Zoe", "Ali", 100]],
    ),
    (
        "variables_debug_004", "remaining_after_purchase",
        "Given balance, price, and quantity, this function is supposed to return "
        "what's left of balance after buying quantity items at price each — but it "
        "has a bug. Find it and fix it.",
        "def remaining_after_purchase(balance, price, quantity):\n"
        "    return balance - price * quantity\n",
        "def remaining_after_purchase(balance, price, quantity):\n"
        "    return balance - price\n",
        [[100, 15, 3], [50, 10, 6], [200, 25, 4]],
    ),
]


def main():
    """Writes all 24 Variables problem files and reports what it did."""
    written = write_topic("variables", "01_variables", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
