"""Writes baseline problem content so every topic has something to load.

A one-time content seeding script that writes a handful of baseline
problems per topic, defined in the PROBLEMS and MORE_PROBLEMS dicts
below, so every topic has navigable content. This is not part of the
shipped app - it's an authoring aid, run once, then more problems get
added by hand or by extending the dicts here.
"""

import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

PROBLEMS = {
    "02_operators": [
        {
            "id": "operators_001",
            "topic": "operators",
            "title": "Area of a rectangle",
            "prompt": "Read width and height (two integers, one per line) and print their product (the area).",
            "starter_code": "width = int(input())\nheight = int(input())\n# compute and print area\n",
            "test_input": "4\n5",
            "expected_output": "20",
            "hint": "Use the * operator to multiply.",
        },
        {
            "id": "operators_002",
            "topic": "operators",
            "title": "Remainder check",
            "prompt": "Read an integer N and print the remainder when N is divided by 3.",
            "starter_code": "n = int(input())\n# print n mod 3\n",
            "test_input": "10",
            "expected_output": "1",
            "hint": "Use the % operator.",
        },
    ],
    "03_io": [
        {
            "id": "io_001",
            "topic": "io",
            "title": "Greet by name",
            "prompt": "Read a name from input and print 'Hello, <name>!'",
            "starter_code": "name = input()\n# print greeting\n",
            "test_input": "Ava",
            "expected_output": "Hello, Ava!",
            "hint": "Use string concatenation or an f-string: f'Hello, {name}!'",
        },
        {
            "id": "io_002",
            "topic": "io",
            "title": "Print on separate lines",
            "prompt": "Read two words (one per line) and print each on its own line, in the order they were entered.",
            "starter_code": "word1 = input()\nword2 = input()\n# print each on its own line\n",
            "test_input": "sun\nmoon",
            "expected_output": "sun\nmoon",
            "hint": "Two separate print() calls.",
        },
    ],
    "04_conditionals": [
        {
            "id": "conditionals_001",
            "topic": "conditionals",
            "title": "Even or odd",
            "prompt": "Read an integer and print 'even' if it's even, otherwise print 'odd'.",
            "starter_code": "n = int(input())\n# print 'even' or 'odd'\n",
            "test_input": "7",
            "expected_output": "odd",
            "hint": "Use n % 2 == 0 to check evenness.",
        },
        {
            "id": "conditionals_002",
            "topic": "conditionals",
            "title": "Largest of two",
            "prompt": "Read two integers (one per line) and print the larger one.",
            "starter_code": "a = int(input())\nb = int(input())\n# print the larger value\n",
            "test_input": "8\n3",
            "expected_output": "8",
            "hint": "if a > b: print(a) else: print(b)",
        },
    ],
    "06_strings": [
        {
            "id": "strings_001",
            "topic": "strings",
            "title": "First character",
            "prompt": "Read a word and print only its first character.",
            "starter_code": "word = input()\n# print the first character\n",
            "test_input": "python",
            "expected_output": "p",
            "hint": "Use indexing: word[0]",
        },
        {
            "id": "strings_002",
            "topic": "strings",
            "title": "Reverse a word",
            "prompt": "Read a word and print it reversed.",
            "starter_code": "word = input()\n# print the reversed word\n",
            "test_input": "hello",
            "expected_output": "olleh",
            "hint": "Slicing with a step of -1 reverses a string: word[::-1]",
        },
    ],
    "07_lists": [
        {
            "id": "lists_001",
            "topic": "lists",
            "title": "Sum a list of numbers",
            "prompt": "Read 3 integers, one per line, store them in a list, then print their sum.",
            "starter_code": "nums = []\nfor _ in range(3):\n    nums.append(int(input()))\n# print the sum\n",
            "test_input": "1\n2\n3",
            "expected_output": "6",
            "hint": "Use sum(nums) or a loop that adds each value.",
        },
        {
            "id": "lists_002",
            "topic": "lists",
            "title": "Largest in a list",
            "prompt": "Read 3 integers into a list and print the largest one.",
            "starter_code": "nums = []\nfor _ in range(3):\n    nums.append(int(input()))\n# print the largest\n",
            "test_input": "4\n9\n2",
            "expected_output": "9",
            "hint": "Use max(nums).",
        },
    ],
    "08_dictionaries": [
        {
            "id": "dictionaries_001",
            "topic": "dictionaries",
            "title": "Look up a value",
            "prompt": "A dictionary ages = {'Sam': 12, 'Al': 15} is provided. Print the age of 'Al'.",
            "starter_code": "ages = {'Sam': 12, 'Al': 15}\n# print ages['Al']\n",
            "test_input": "",
            "expected_output": "15",
            "hint": "Access with ages['Al']",
        },
        {
            "id": "dictionaries_002",
            "topic": "dictionaries",
            "title": "Count with a dictionary",
            "prompt": "A dictionary scores = {'math': 90, 'art': 85, 'gym': 95} is provided. Print how many keys it has.",
            "starter_code": "scores = {'math': 90, 'art': 85, 'gym': 95}\n# print number of keys\n",
            "test_input": "",
            "expected_output": "3",
            "hint": "Use len(scores).",
        },
    ],
    "09_tuples": [
        {
            "id": "tuples_001",
            "topic": "tuples",
            "title": "Access tuple elements",
            "prompt": "A tuple point = (3, 7) is provided. Print the two values separated by a space, in the format 'x y'.",
            "starter_code": "point = (3, 7)\n# print point[0] and point[1] separated by a space\n",
            "test_input": "",
            "expected_output": "3 7",
            "hint": "print(point[0], point[1])",
        },
        {
            "id": "tuples_002",
            "topic": "tuples",
            "title": "Unpack a tuple",
            "prompt": "A tuple pair = (5, 10) is provided. Unpack it into variables a and b, then print their sum.",
            "starter_code": "pair = (5, 10)\n# unpack pair into a, b and print their sum\n",
            "test_input": "",
            "expected_output": "15",
            "hint": "a, b = pair",
        },
    ],
    "10_nested": [
        {
            "id": "nested_001",
            "topic": "nested",
            "title": "List of lists",
            "prompt": "grid = [[1, 2], [3, 4]] is provided. Print the value at row 1, column 0 (i.e. grid[1][0]).",
            "starter_code": "grid = [[1, 2], [3, 4]]\n# print grid[1][0]\n",
            "test_input": "",
            "expected_output": "3",
            "hint": "Index twice: grid[1][0]",
        },
        {
            "id": "nested_002",
            "topic": "nested",
            "title": "List of dictionaries",
            "prompt": "students = [{'name': 'Ana'}, {'name': 'Leo'}] is provided. Print the name of the second student.",
            "starter_code": "students = [{'name': 'Ana'}, {'name': 'Leo'}]\n# print the name of the second student\n",
            "test_input": "",
            "expected_output": "Leo",
            "hint": "students[1]['name']",
        },
    ],
}


MORE_PROBLEMS = {
    "01_variables": [
        {
            "id": "variables_003",
            "topic": "variables",
            "title": "Convert to float",
            "prompt": "Read an integer and print it as a float (e.g. 5 becomes 5.0).",
            "starter_code": "n = int(input())\n# print n as a float\n",
            "test_input": "5",
            "expected_output": "5.0",
            "hint": "Use float(n).",
        },
        {
            "id": "variables_004",
            "topic": "variables",
            "title": "Boolean from comparison",
            "prompt": "Read two integers (one per line) and print True if the first is greater than the second, otherwise False.",
            "starter_code": "a = int(input())\nb = int(input())\n# print the boolean result of a > b\n",
            "test_input": "9\n4",
            "expected_output": "True",
            "hint": "print(a > b) prints a boolean directly.",
        },
        {
            "id": "variables_005",
            "topic": "variables",
            "title": "String length",
            "prompt": "Read a word and print how many characters it has.",
            "starter_code": "word = input()\n# print the length of word\n",
            "test_input": "banana",
            "expected_output": "6",
            "hint": "Use len(word).",
        },
    ],
    "02_operators": [
        {
            "id": "operators_003",
            "topic": "operators",
            "title": "Integer division",
            "prompt": "Read two integers a and b (one per line) and print a divided by b using integer (floor) division.",
            "starter_code": "a = int(input())\nb = int(input())\n# print integer division of a by b\n",
            "test_input": "17\n5",
            "expected_output": "3",
            "hint": "Use the // operator.",
        },
        {
            "id": "operators_004",
            "topic": "operators",
            "title": "Exponent",
            "prompt": "Read an integer base and an integer exponent (one per line), print base raised to that exponent.",
            "starter_code": "base = int(input())\nexp = int(input())\n# print base ** exp\n",
            "test_input": "2\n5",
            "expected_output": "32",
            "hint": "Use the ** operator.",
        },
        {
            "id": "operators_005",
            "topic": "operators",
            "title": "Combine comparisons",
            "prompt": "Read an integer N. Print True if N is between 1 and 10 (inclusive), otherwise False.",
            "starter_code": "n = int(input())\n# print True if 1 <= n <= 10 else False\n",
            "test_input": "7",
            "expected_output": "True",
            "hint": "Python allows chained comparisons: 1 <= n <= 10",
        },
    ],
    "03_io": [
        {
            "id": "io_003",
            "topic": "io",
            "title": "Print with separator",
            "prompt": "Read two words (one per line) and print them on the same line separated by a comma and a space.",
            "starter_code": "word1 = input()\nword2 = input()\n# print 'word1, word2'\n",
            "test_input": "cats\ndogs",
            "expected_output": "cats, dogs",
            "hint": "print(word1 + ', ' + word2) or use the sep argument of print().",
        },
        {
            "id": "io_004",
            "topic": "io",
            "title": "Read a number and echo it",
            "prompt": "Read a float and print it back exactly as read.",
            "starter_code": "value = float(input())\n# print value\n",
            "test_input": "3.14",
            "expected_output": "3.14",
            "hint": "print(value) will print the float value.",
        },
        {
            "id": "io_005",
            "topic": "io",
            "title": "Formatted output",
            "prompt": "Read a name and an age (one per line, age as an integer). Print 'NAME is AGE years old.'",
            "starter_code": "name = input()\nage = int(input())\n# print formatted sentence\n",
            "test_input": "Maya\n14",
            "expected_output": "Maya is 14 years old.",
            "hint": "Use an f-string: f'{name} is {age} years old.'",
        },
    ],
    "04_conditionals": [
        {
            "id": "conditionals_003",
            "topic": "conditionals",
            "title": "Grade classifier",
            "prompt": "Read an integer score. Print 'pass' if score is 60 or above, otherwise print 'fail'.",
            "starter_code": "score = int(input())\n# print 'pass' or 'fail'\n",
            "test_input": "72",
            "expected_output": "pass",
            "hint": "if score >= 60: print('pass')",
        },
        {
            "id": "conditionals_004",
            "topic": "conditionals",
            "title": "Sign of a number",
            "prompt": "Read an integer and print 'positive', 'negative', or 'zero' depending on its sign.",
            "starter_code": "n = int(input())\n# print 'positive', 'negative', or 'zero'\n",
            "test_input": "-5",
            "expected_output": "negative",
            "hint": "Use if/elif/else with n > 0, n < 0, and the remaining case.",
        },
        {
            "id": "conditionals_005",
            "topic": "conditionals",
            "title": "Divisible by both",
            "prompt": "Read an integer N. Print 'yes' if N is divisible by both 2 and 3, otherwise print 'no'.",
            "starter_code": "n = int(input())\n# print 'yes' or 'no'\n",
            "test_input": "12",
            "expected_output": "yes",
            "hint": "Use the % operator with and: n % 2 == 0 and n % 3 == 0",
        },
    ],
    "05_loops": [
        {
            "id": "loops_002",
            "topic": "loops",
            "title": "Count down",
            "prompt": "Read an integer N and print the numbers from N down to 1, each on its own line.",
            "starter_code": "n = int(input())\n# print n, n-1, ..., 1 each on its own line\n",
            "test_input": "4",
            "expected_output": "4\n3\n2\n1",
            "hint": "Use range(n, 0, -1)",
        },
        {
            "id": "loops_003",
            "topic": "loops",
            "title": "Multiplication table row",
            "prompt": "Read an integer N and print N * 1 through N * 5, each result on its own line.",
            "starter_code": "n = int(input())\n# print n*1 through n*5, one per line\n",
            "test_input": "3",
            "expected_output": "3\n6\n9\n12\n15",
            "hint": "for i in range(1, 6): print(n * i)",
        },
        {
            "id": "loops_004",
            "topic": "loops",
            "title": "Count even numbers",
            "prompt": "Read an integer N. Print how many even numbers are in the range 1 to N (inclusive).",
            "starter_code": "n = int(input())\ncount = 0\n# loop and count even numbers\nprint(count)\n",
            "test_input": "10",
            "expected_output": "5",
            "hint": "Inside the loop: if i % 2 == 0: count += 1",
        },
    ],
    "06_strings": [
        {
            "id": "strings_003",
            "topic": "strings",
            "title": "Uppercase a word",
            "prompt": "Read a word and print it in all uppercase letters.",
            "starter_code": "word = input()\n# print word in uppercase\n",
            "test_input": "hello",
            "expected_output": "HELLO",
            "hint": "Use word.upper()",
        },
        {
            "id": "strings_004",
            "topic": "strings",
            "title": "Count a character",
            "prompt": "Read a word and print how many times the letter 'a' appears in it.",
            "starter_code": "word = input()\n# print count of 'a' in word\n",
            "test_input": "banana",
            "expected_output": "3",
            "hint": "Use word.count('a')",
        },
        {
            "id": "strings_005",
            "topic": "strings",
            "title": "Slice a substring",
            "prompt": "Read a word and print the first 3 characters.",
            "starter_code": "word = input()\n# print the first 3 characters\n",
            "test_input": "elephant",
            "expected_output": "ele",
            "hint": "Use slicing: word[:3]",
        },
    ],
    "07_lists": [
        {
            "id": "lists_003",
            "topic": "lists",
            "title": "Build a list with append",
            "prompt": "Read 4 integers, one per line, appending each to a list, then print the full list.",
            "starter_code": "nums = []\nfor _ in range(4):\n    nums.append(int(input()))\n# print the list\n",
            "test_input": "1\n2\n3\n4",
            "expected_output": "[1, 2, 3, 4]",
            "hint": "print(nums) prints the whole list.",
        },
        {
            "id": "lists_004",
            "topic": "lists",
            "title": "Access by index",
            "prompt": "A list values = [10, 20, 30, 40] is provided. Print the element at index 2.",
            "starter_code": "values = [10, 20, 30, 40]\n# print values[2]\n",
            "test_input": "",
            "expected_output": "30",
            "hint": "Indexing starts at 0, so index 2 is the third element.",
        },
        {
            "id": "lists_005",
            "topic": "lists",
            "title": "List length",
            "prompt": "A list items = ['a', 'b', 'c', 'd', 'e'] is provided. Print how many elements it has.",
            "starter_code": "items = ['a', 'b', 'c', 'd', 'e']\n# print the length\n",
            "test_input": "",
            "expected_output": "5",
            "hint": "Use len(items).",
        },
    ],
    "08_dictionaries": [
        {
            "id": "dictionaries_003",
            "topic": "dictionaries",
            "title": "Add a key",
            "prompt": "A dictionary d = {'a': 1} is provided. Add the key 'b' with value 2, then print the full dictionary.",
            "starter_code": "d = {'a': 1}\n# add key 'b' with value 2, then print d\n",
            "test_input": "",
            "expected_output": "{'a': 1, 'b': 2}",
            "hint": "d['b'] = 2",
        },
        {
            "id": "dictionaries_004",
            "topic": "dictionaries",
            "title": "Check key existence",
            "prompt": "A dictionary colors = {'sky': 'blue', 'grass': 'green'} is provided. Print True if 'sky' is a key, otherwise False.",
            "starter_code": "colors = {'sky': 'blue', 'grass': 'green'}\n# print True or False\n",
            "test_input": "",
            "expected_output": "True",
            "hint": "Use the in operator: 'sky' in colors",
        },
        {
            "id": "dictionaries_005",
            "topic": "dictionaries",
            "title": "Update a value",
            "prompt": "A dictionary stock = {'apples': 5} is provided. Update 'apples' to 8, then print the value.",
            "starter_code": "stock = {'apples': 5}\n# update 'apples' to 8, then print it\n",
            "test_input": "",
            "expected_output": "8",
            "hint": "stock['apples'] = 8",
        },
    ],
    "09_tuples": [
        {
            "id": "tuples_003",
            "topic": "tuples",
            "title": "Tuple length",
            "prompt": "A tuple values = (3, 6, 9, 12) is provided. Print how many elements it has.",
            "starter_code": "values = (3, 6, 9, 12)\n# print the length\n",
            "test_input": "",
            "expected_output": "4",
            "hint": "Use len(values).",
        },
        {
            "id": "tuples_004",
            "topic": "tuples",
            "title": "Tuple in a loop",
            "prompt": "A tuple nums = (1, 2, 3) is provided. Print each value on its own line.",
            "starter_code": "nums = (1, 2, 3)\n# print each value on its own line\n",
            "test_input": "",
            "expected_output": "1\n2\n3",
            "hint": "for n in nums: print(n)",
        },
        {
            "id": "tuples_005",
            "topic": "tuples",
            "title": "Three-way unpack",
            "prompt": "A tuple rgb = (255, 0, 128) is provided. Unpack it into r, g, b and print them separated by spaces.",
            "starter_code": "rgb = (255, 0, 128)\n# unpack into r, g, b and print\n",
            "test_input": "",
            "expected_output": "255 0 128",
            "hint": "r, g, b = rgb",
        },
    ],
    "10_nested": [
        {
            "id": "nested_003",
            "topic": "nested",
            "title": "Sum a nested list",
            "prompt": "matrix = [[1, 2], [3, 4], [5, 6]] is provided. Print the sum of all numbers in the matrix.",
            "starter_code": "matrix = [[1, 2], [3, 4], [5, 6]]\ntotal = 0\n# loop through rows and columns, adding to total\nprint(total)\n",
            "test_input": "",
            "expected_output": "21",
            "hint": "Nested for loops: for row in matrix: for val in row: total += val",
        },
        {
            "id": "nested_004",
            "topic": "nested",
            "title": "Dictionary of lists",
            "prompt": "scores = {'Sam': [90, 85], 'Al': [70, 75]} is provided. Print the second score for 'Sam'.",
            "starter_code": "scores = {'Sam': [90, 85], 'Al': [70, 75]}\n# print the second score for Sam\n",
            "test_input": "",
            "expected_output": "85",
            "hint": "scores['Sam'][1]",
        },
        {
            "id": "nested_005",
            "topic": "nested",
            "title": "List of tuples",
            "prompt": "points = [(1, 2), (3, 4), (5, 6)] is provided. Print the y-value (second item) of the last point.",
            "starter_code": "points = [(1, 2), (3, 4), (5, 6)]\n# print the y-value of the last point\n",
            "test_input": "",
            "expected_output": "6",
            "hint": "points[-1][1] uses negative indexing to get the last item.",
        },
    ],
}


def main():
    """Writes every problem in PROBLEMS and MORE_PROBLEMS out as JSON files.

    Creates each topic's content/<NN>_<topic>/ folder if it doesn't
    already exist, then writes one <id>.json file per problem.
    """
    total = 0
    all_problems = {**PROBLEMS}
    for folder_name, extra in MORE_PROBLEMS.items():
        all_problems.setdefault(folder_name, [])
        all_problems[folder_name] = all_problems[folder_name] + extra
    for folder_name, problems in all_problems.items():
        folder = CONTENT_DIR / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        for problem in problems:
            out_path = folder / f"{problem['id']}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(problem, f, indent=2)
            total += 1
    print(f"Wrote {total} problem files across {len(all_problems)} topics.")


if __name__ == "__main__":
    main()
