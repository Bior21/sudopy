"""Hand-written correct solutions, one per problem.

SOLUTIONS is the single source of truth for "what does a correct answer
to this problem look like" - verify_all_solvable.py imports it to check
every problem's expected_output actually matches what correct code
produces, and gui/problem_view.py's Show Solution button imports it to
reveal a solution to a student who has already attempted the problem.

Each entry is one of two shapes, and verify_all_solvable.py tells them
apart by whether the text starts with "def ": a plain top-level script
(the legacy I/O-topic style, run directly through core.runner since it
reads via input() rather than taking arguments), or a real function
definition matching the problem's function_name (every other topic,
run through core.submission exactly like a student submission would be,
since it takes its test data as arguments).
"""

SOLUTIONS = {
    "operators_001": "width = int(input())\nheight = int(input())\nprint(width * height)\n",
    "operators_002": "n = int(input())\nprint(n % 3)\n",
    "io_001": "name = input()\nprint(f'Hello, {name}!')\n",
    "io_002": "word1 = input()\nword2 = input()\nprint(word1)\nprint(word2)\n",
    "conditionals_001": "n = int(input())\nif n % 2 == 0:\n    print('even')\nelse:\n    print('odd')\n",
    "conditionals_002": "a = int(input())\nb = int(input())\nif a > b:\n    print(a)\nelse:\n    print(b)\n",
    "strings_001": "word = input()\nprint(word[0])\n",
    "strings_002": "word = input()\nprint(word[::-1])\n",
    "lists_001": "nums = []\nfor _ in range(3):\n    nums.append(int(input()))\nprint(sum(nums))\n",
    "lists_002": "nums = []\nfor _ in range(3):\n    nums.append(int(input()))\nprint(max(nums))\n",
    "dictionaries_001": "ages = {'Sam': 12, 'Al': 15}\nprint(ages['Al'])\n",
    "dictionaries_002": "scores = {'math': 90, 'art': 85, 'gym': 95}\nprint(len(scores))\n",
    "tuples_001": "point = (3, 7)\nprint(point[0], point[1])\n",
    "tuples_002": "pair = (5, 10)\na, b = pair\nprint(a + b)\n",
    "nested_001": "grid = [[1, 2], [3, 4]]\nprint(grid[1][0])\n",
    "nested_002": "students = [{'name': 'Ana'}, {'name': 'Leo'}]\nprint(students[1]['name'])\n",
    "operators_003": "a = int(input())\nb = int(input())\nprint(a // b)\n",
    "operators_004": "base = int(input())\nexp = int(input())\nprint(base ** exp)\n",
    "operators_005": "n = int(input())\nprint(1 <= n <= 10)\n",
    "io_003": "word1 = input()\nword2 = input()\nprint(word1 + ', ' + word2)\n",
    "io_004": "value = float(input())\nprint(value)\n",
    "io_005": "name = input()\nage = int(input())\nprint(f'{name} is {age} years old.')\n",
    "conditionals_003": "score = int(input())\nif score >= 60:\n    print('pass')\nelse:\n    print('fail')\n",
    "conditionals_004": "n = int(input())\nif n > 0:\n    print('positive')\nelif n < 0:\n    print('negative')\nelse:\n    print('zero')\n",
    "conditionals_005": "n = int(input())\nif n % 2 == 0 and n % 3 == 0:\n    print('yes')\nelse:\n    print('no')\n",
    "strings_003": "word = input()\nprint(word.upper())\n",
    "strings_004": "word = input()\nprint(word.count('a'))\n",
    "strings_005": "word = input()\nprint(word[:3])\n",
    "lists_003": "nums = []\nfor _ in range(4):\n    nums.append(int(input()))\nprint(nums)\n",
    "lists_004": "values = [10, 20, 30, 40]\nprint(values[2])\n",
    "lists_005": "items = ['a', 'b', 'c', 'd', 'e']\nprint(len(items))\n",
    "dictionaries_003": "d = {'a': 1}\nd['b'] = 2\nprint(d)\n",
    "dictionaries_004": "colors = {'sky': 'blue', 'grass': 'green'}\nprint('sky' in colors)\n",
    "dictionaries_005": "stock = {'apples': 5}\nstock['apples'] = 8\nprint(stock['apples'])\n",
    "tuples_003": "values = (3, 6, 9, 12)\nprint(len(values))\n",
    "tuples_004": "nums = (1, 2, 3)\nfor n in nums:\n    print(n)\n",
    "tuples_005": "rgb = (255, 0, 128)\nr, g, b = rgb\nprint(r, g, b)\n",
    "nested_003": "matrix = [[1, 2], [3, 4], [5, 6]]\ntotal = 0\nfor row in matrix:\n    for val in row:\n        total += val\nprint(total)\n",
    "nested_004": "scores = {'Sam': [90, 85], 'Al': [70, 75]}\nprint(scores['Sam'][1])\n",
    "nested_005": "points = [(1, 2), (3, 4), (5, 6)]\nprint(points[-1][1])\n",

    # Loops (05_loops): function-based, since these problems take arguments
    # instead of reading via input() - see core/submission.py for why a
    # solution shaped like "def name(...): ... return ..." is run through
    # run_and_grade_all rather than run_code directly.
    "loops_001": "def sum_of_odd_numbers_up_to(n):\n    total = 0\n    for i in range(1, n + 1):\n        if i % 2 == 1:\n            total += i\n    return total\n",
    "loops_002": "def count_divisible_by(n, divisor):\n    count = 0\n    for i in range(1, n + 1):\n        if i % divisor == 0:\n            count += 1\n    return count\n",
    "loops_003": "def sum_of_range(start, end):\n    total = 0\n    for i in range(start, end + 1):\n        total += i\n    return total\n",
    "loops_004": "def multiplication_table(n):\n    table = []\n    for i in range(1, 6):\n        table.append(n * i)\n    return table\n",
    "loops_005": "def countdown_by_step(n, step):\n    result = []\n    current = n\n    while current >= 0:\n        result.append(current)\n        current -= step\n    return result\n",
    "loops_006": "def factorial(n):\n    total = 1\n    for i in range(1, n + 1):\n        total *= i\n    return total\n",
    "loops_007": "def digit_sum(n):\n    total = 0\n    while n > 0:\n        total += n % 10\n        n //= 10\n    return total\n",
    "loops_008": "def count_digits(n):\n    count = 0\n    while n > 0:\n        count += 1\n        n //= 10\n    return count\n",
    "loops_009": "def reverse_number(n):\n    reversed_n = 0\n    while n > 0:\n        digit = n % 10\n        reversed_n = reversed_n * 10 + digit\n        n //= 10\n    return reversed_n\n",
    "loops_010": "def number_triangle(n):\n    rows = []\n    for i in range(1, n + 1):\n        row = ''\n        for x in range(1, i + 1):\n            if x > 1:\n                row = row + ' '\n            row = row + str(x)\n        rows.append(row)\n    return '\\n'.join(rows)\n",
    "loops_011": "def count_vowels(word):\n    vowels = 'aeiouAEIOU'\n    count = 0\n    for ch in word:\n        if ch in vowels:\n            count += 1\n    return count\n",
    "loops_012": "def count_occurrences(word, letter):\n    count = 0\n    for ch in word:\n        if ch == letter:\n            count += 1\n    return count\n",
    "loops_013": "def sum_of_multiples_of_either(limit, a, b):\n    total = 0\n    for i in range(1, limit):\n        if i % a == 0 or i % b == 0:\n            total += i\n    return total\n",
    "loops_014": "def power_without_operator(base, exp):\n    result = 1\n    for i in range(exp):\n        result *= base\n    return result\n",
    "loops_015": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, n):\n        if n % i == 0:\n            return False\n    return True\n",
    "loops_016": "def gcd_of_two(a, b):\n    while b != 0:\n        a, b = b, a % b\n    return a\n",
    "loops_017": "def fibonacci_at(n):\n    a, b = 0, 1\n    for i in range(n):\n        a, b = b, a + b\n    return a\n",
    "loops_018": "def digital_root(n):\n    while n >= 10:\n        total = 0\n        while n > 0:\n            total += n % 10\n            n //= 10\n        n = total\n    return n\n",
    "loops_019": "def triangle_pattern(n):\n    rows = []\n    for i in range(1, n + 1):\n        rows.append('*' * i)\n    return '\\n'.join(rows)\n",
    "loops_020": "def collatz_steps(n):\n    steps = 0\n    while n != 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        steps += 1\n    return steps\n",
    "loops_debug_001": "def sum_of_range(start, end):\n    total = 0\n    for i in range(start, end + 1):\n        total += i\n    return total\n",
    "loops_debug_002": "def factorial(n):\n    total = 1\n    for i in range(1, n + 1):\n        total *= i\n    return total\n",
    "loops_debug_003": "def count_divisible_by(n, divisor):\n    count = 0\n    for i in range(1, n + 1):\n        if i % divisor == 0:\n            count += 1\n    return count\n",
    "loops_debug_004": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, n):\n        if n % i == 0:\n            return False\n    return True\n",

    # Variables (01_variables)
    "variables_001": "def total_after_tax(price, tax_rate):\n    return price + price * tax_rate\n",
    "variables_002": "def temperature_swing(morning_temp, evening_temp):\n    return evening_temp - morning_temp\n",
    "variables_003": "def time_to_seconds(hours, minutes):\n    return hours * 3600 + minutes * 60\n",
    "variables_004": "def split_the_bill_with_tip(total, people, tip_rate):\n    return (total + total * tip_rate) / people\n",
    "variables_005": "def age_gap(age1, age2):\n    return abs(age1 - age2)\n",
    "variables_006": "def exceeds_when_converted(celsius, fahrenheit_limit):\n    fahrenheit = celsius * 9 / 5 + 32\n    return fahrenheit > fahrenheit_limit\n",
    "variables_007": "def remaining_after_purchase(balance, price, quantity):\n    return balance - price * quantity\n",
    "variables_008": "def paces_to_meters(paces, pace_length):\n    return paces * pace_length\n",
    "variables_009": "def is_within_one_year(age1, age2):\n    return abs(age1 - age2) <= 1\n",
    "variables_010": "def formatted_id(first, last, id_number):\n    return f'{last}, {first} (#{id_number})'\n",
    "variables_011": "def discounted_price(price, discount_percent):\n    return price - price * discount_percent / 100\n",
    "variables_012": "def speed_from_distance_time(distance, time):\n    return distance / time\n",
    "variables_013": "def total_distance_two_legs(speed1, time1, speed2, time2):\n    return speed1 * time1 + speed2 * time2\n",
    "variables_014": "def profit(revenue, cost):\n    return revenue - cost\n",
    "variables_015": "def year_someone_turns_age(birth_year, target_age):\n    return birth_year + target_age\n",
    "variables_016": "def flag_to_bit(is_active):\n    return int(is_active)\n",
    "variables_017": "def average_speed(distance, time1, time2):\n    return distance / (time1 + time2)\n",
    "variables_018": "def can_afford(balance, price):\n    return balance >= price\n",
    "variables_019": "def total_inches(feet, inches):\n    return feet * 12 + inches\n",
    "variables_020": "def net_change(start_value, end_value):\n    return end_value - start_value\n",
    "variables_debug_001": "def speed_from_distance_time(distance, time):\n    return distance / time\n",
    "variables_debug_002": "def discounted_price(price, discount_percent):\n    return price - price * discount_percent / 100\n",
    "variables_debug_003": "def formatted_id(first, last, id_number):\n    return f'{last}, {first} (#{id_number})'\n",
    "variables_debug_004": "def remaining_after_purchase(balance, price, quantity):\n    return balance - price * quantity\n",
}
