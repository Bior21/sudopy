"""Hand-written correct solutions, one per problem.

SOLUTIONS is the single source of truth for "what does a correct answer
to this problem look like" - verify_all_solvable.py imports it to check
every problem's expected_output actually matches what correct code
produces, and gui/problem_view.py's Show Solution button imports it to
reveal a solution to a student who has already attempted the problem.
Kept as plain top-level scripts (not function-wrapped, unlike
starter_code), since they're run directly through core.runner rather
than through core.submission's function-call wrapping.
"""

SOLUTIONS = {
    "variables_001": "age = int(input())\nprint(age)\n",
    "variables_002": "a = int(input())\nb = int(input())\na, b = b, a\nprint(a, b)\n",
    "operators_001": "width = int(input())\nheight = int(input())\nprint(width * height)\n",
    "operators_002": "n = int(input())\nprint(n % 3)\n",
    "io_001": "name = input()\nprint(f'Hello, {name}!')\n",
    "io_002": "word1 = input()\nword2 = input()\nprint(word1)\nprint(word2)\n",
    "conditionals_001": "n = int(input())\nif n % 2 == 0:\n    print('even')\nelse:\n    print('odd')\n",
    "conditionals_002": "a = int(input())\nb = int(input())\nif a > b:\n    print(a)\nelse:\n    print(b)\n",
    "loops_001": "n = int(input())\ntotal = 0\nfor i in range(1, n + 1):\n    total += i\nprint(total)\n",
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
    "variables_003": "n = int(input())\nprint(float(n))\n",
    "variables_004": "a = int(input())\nb = int(input())\nprint(a > b)\n",
    "variables_005": "word = input()\nprint(len(word))\n",
    "operators_003": "a = int(input())\nb = int(input())\nprint(a // b)\n",
    "operators_004": "base = int(input())\nexp = int(input())\nprint(base ** exp)\n",
    "operators_005": "n = int(input())\nprint(1 <= n <= 10)\n",
    "io_003": "word1 = input()\nword2 = input()\nprint(word1 + ', ' + word2)\n",
    "io_004": "value = float(input())\nprint(value)\n",
    "io_005": "name = input()\nage = int(input())\nprint(f'{name} is {age} years old.')\n",
    "conditionals_003": "score = int(input())\nif score >= 60:\n    print('pass')\nelse:\n    print('fail')\n",
    "conditionals_004": "n = int(input())\nif n > 0:\n    print('positive')\nelif n < 0:\n    print('negative')\nelse:\n    print('zero')\n",
    "conditionals_005": "n = int(input())\nif n % 2 == 0 and n % 3 == 0:\n    print('yes')\nelse:\n    print('no')\n",
    "loops_002": "n = int(input())\nfor i in range(n, 0, -1):\n    print(i)\n",
    "loops_003": "n = int(input())\nfor i in range(1, 6):\n    print(n * i)\n",
    "loops_004": "n = int(input())\ncount = 0\nfor i in range(1, n + 1):\n    if i % 2 == 0:\n        count += 1\nprint(count)\n",
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
}
