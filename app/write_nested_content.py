"""One-time authoring script: writes the redesigned Nested topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py. Like write_tuples_content.py, list_of_pairs_to_dict
passes real Python tuples so its call site shows authentic tuple syntax -
see content_authoring.py's _encode_tuples.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "nested_001", "get_grid_value",
        "Given a 2D grid (a list of lists) and a row/col index, return the "
        "value at that position. "
        "e.g. grid=[[1, 2], [3, 4]], row=1, col=0 returns 3.",
        "def get_grid_value(grid, row, col):\n    return grid[row][col]\n",
        [[[[1, 2], [3, 4]], 1, 0], [[[5, 6, 7]], 0, 2], [[[1], [2], [3]], 2, 0]],
        "",
    ),
    (
        "nested_002", "sum_of_grid",
        "Given a 2D grid, return the sum of every value in it. "
        "e.g. grid=[[1, 2], [3, 4]] returns 10.",
        "def sum_of_grid(grid):\n"
        "    total = 0\n"
        "    for row in grid:\n"
        "        for val in row:\n            total += val\n"
        "    return total\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 2, 3], [4, 5, 6]]]],
        "",
    ),
    (
        "nested_003", "flatten_grid",
        "Given a 2D grid, return a single list with every value, row by row. "
        "e.g. grid=[[1, 2], [3, 4]] returns [1, 2, 3, 4].",
        "def flatten_grid(grid):\n"
        "    result = []\n"
        "    for row in grid:\n"
        "        for val in row:\n            result.append(val)\n"
        "    return result\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 2], [3], [4, 5, 6]]]],
        "",
    ),
    (
        "nested_004", "row_sums",
        "Given a 2D grid, return a list with the sum of each row, in order. "
        "e.g. grid=[[1, 2], [3, 4]] returns [3, 7].",
        "def row_sums(grid):\n"
        "    result = []\n"
        "    for row in grid:\n        result.append(sum(row))\n"
        "    return result\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 2, 3], [4, 5, 6]]]],
        "",
    ),
    (
        "nested_005", "column_sum",
        "Given a 2D grid and a col_index, return the sum of that column "
        "across every row. e.g. grid=[[1, 2], [3, 4]], col_index=1 returns 6.",
        "def column_sum(grid, col_index):\n"
        "    total = 0\n"
        "    for row in grid:\n        total += row[col_index]\n"
        "    return total\n",
        [[[[1, 2], [3, 4]], 0], [[[1, 2], [3, 4]], 1], [[[5, 6, 7], [8, 9, 10]], 2]],
        "",
    ),
    (
        "nested_006", "transpose_grid",
        "Given a 2D grid, return it transposed - rows become columns. "
        "e.g. grid=[[1, 2], [3, 4]] returns [[1, 3], [2, 4]].",
        "def transpose_grid(grid):\n"
        "    result = []\n"
        "    for col in range(len(grid[0])):\n"
        "        new_row = []\n"
        "        for row in grid:\n            new_row.append(row[col])\n"
        "        result.append(new_row)\n"
        "    return result\n",
        [[[[1, 2], [3, 4]]], [[[1, 2, 3]]], [[[1], [2], [3]]]],
        "The transposed grid has one new row per column of the original - loop col over range(len(grid[0])), then pick out row[col] from every row.",
    ),
    (
        "nested_007", "max_in_grid",
        "Given a 2D grid, return its largest value. "
        "e.g. grid=[[1, 5], [3, 2]] returns 5.",
        "def max_in_grid(grid):\n"
        "    best = grid[0][0]\n"
        "    for row in grid:\n"
        "        for val in row:\n"
        "            if val > best:\n                best = val\n"
        "    return best\n",
        [[[[1, 5], [3, 2]]], [[[-1, -5], [-3, -2]]], [[[7]]]],
        "",
    ),
    (
        "nested_008", "count_matching_in_grid",
        "Given a 2D grid and a target, return how many times target appears "
        "anywhere in the grid. "
        "e.g. grid=[[1, 2, 1], [3, 1, 2]], target=1 returns 3.",
        "def count_matching_in_grid(grid, target):\n"
        "    count = 0\n"
        "    for row in grid:\n"
        "        for val in row:\n"
        "            if val == target:\n                count += 1\n"
        "    return count\n",
        [[[[1, 2, 1], [3, 1, 2]], 1], [[[5, 6]], 9], [[[4, 4], [4, 4]], 4]],
        "",
    ),
    (
        "nested_009", "diagonal_sum",
        "Given a square 2D grid, return the sum of its main diagonal - "
        "grid[0][0], grid[1][1], and so on. "
        "e.g. grid=[[1, 2], [3, 4]] returns 5.",
        "def diagonal_sum(grid):\n"
        "    total = 0\n"
        "    for i in range(len(grid)):\n        total += grid[i][i]\n"
        "    return total\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 0, 0], [0, 2, 0], [0, 0, 3]]]],
        "",
    ),
    (
        "nested_010", "get_student_field",
        "Given a list of student dictionaries and an index and field name, "
        "return that student's value for that field. "
        "e.g. students=[{'name': 'Ana', 'score': 90}, {'name': 'Leo', "
        "'score': 85}], index=1, field='name' returns 'Leo'.",
        "def get_student_field(students, index, field):\n"
        "    return students[index][field]\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 85}], 1, "name"],
            [[{"name": "Sam", "score": 70}], 0, "score"],
            [[{"name": "Al", "score": 95}, {"name": "Kim", "score": 88}], 0, "score"],
        ],
        "",
    ),
    (
        "nested_011", "total_score",
        "Given a list of student dictionaries and a field name, return the "
        "sum of that field across every student. "
        "e.g. students=[{'score': 90}, {'score': 85}], field='score' "
        "returns 175.",
        "def total_score(students, field):\n"
        "    total = 0\n"
        "    for s in students:\n        total += s[field]\n"
        "    return total\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 85}], "score"],
            [[{"score": 100}], "score"],
            [[{"score": 10}, {"score": 20}, {"score": 30}], "score"],
        ],
        "",
    ),
    (
        "nested_012", "names_of_students",
        "Given a list of student dictionaries, return a list of just their "
        "names. e.g. students=[{'name': 'Ana'}, {'name': 'Leo'}] returns "
        "['Ana', 'Leo'].",
        "def names_of_students(students):\n"
        "    result = []\n"
        "    for s in students:\n        result.append(s['name'])\n"
        "    return result\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 85}]],
            [[{"name": "Sam", "score": 70}]],
            [[{"name": "Al"}, {"name": "Kim"}]],
        ],
        "",
    ),
    (
        "nested_013", "filter_students_by_min_score",
        "Given a list of student dictionaries and a min_score, return the "
        "names of every student whose score is at least min_score. "
        "e.g. students=[{'name': 'Ana', 'score': 90}, {'name': 'Leo', "
        "'score': 60}], min_score=70 returns ['Ana'].",
        "def filter_students_by_min_score(students, min_score):\n"
        "    result = []\n"
        "    for s in students:\n"
        "        if s['score'] >= min_score:\n            result.append(s['name'])\n"
        "    return result\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 60}], 70],
            [[{"name": "Sam", "score": 50}], 70],
            [[{"name": "Al", "score": 95}, {"name": "Kim", "score": 95}], 95],
        ],
        "",
    ),
    (
        "nested_014", "average_field",
        "Given a list of student dictionaries and a field name, return the "
        "average of that field across every student. "
        "e.g. students=[{'score': 80}, {'score': 90}, {'score': 100}], "
        "field='score' returns 90.0.",
        "def average_field(students, field):\n"
        "    total = 0\n"
        "    for s in students:\n        total += s[field]\n"
        "    return total / len(students)\n",
        [
            [[{"score": 80}, {"score": 90}, {"score": 100}], "score"],
            [[{"score": 50}], "score"],
            [[{"score": 10}, {"score": 20}], "score"],
        ],
        "",
    ),
    (
        "nested_015", "get_nested_dict_value",
        "Given a dictionary of dictionaries and an outer_key and inner_key, "
        "return the value found by looking up both in turn. "
        "e.g. data={'Sam': {'math': 90, 'art': 85}}, outer_key='Sam', "
        "inner_key='art' returns 85.",
        "def get_nested_dict_value(data, outer_key, inner_key):\n"
        "    return data[outer_key][inner_key]\n",
        [
            [{"Sam": {"math": 90, "art": 85}}, "Sam", "art"],
            [{"Al": {"gym": 70}}, "Al", "gym"],
            [{"A": {"x": 1}, "B": {"x": 2}}, "B", "x"],
        ],
        "",
    ),
    (
        "nested_016", "add_score_to_student",
        "Given a list of student dictionaries, an index, and a number of "
        "points, add points to that student's score and return the list. "
        "e.g. students=[{'name': 'Ana', 'score': 90}], index=0, points=5 "
        "returns [{'name': 'Ana', 'score': 95}].",
        "def add_score_to_student(students, index, points):\n"
        "    students[index]['score'] += points\n"
        "    return students\n",
        [
            [[{"name": "Ana", "score": 90}], 0, 5],
            [[{"name": "Sam", "score": 50}, {"name": "Al", "score": 60}], 1, 10],
            [[{"name": "X", "score": 0}], 0, 100],
        ],
        "",
    ),
    (
        "nested_017", "group_totals",
        "Given a dictionary mapping each group name to a list of numbers, "
        "return a new dictionary mapping each group name to the sum of its "
        "list. e.g. groups={'a': [1, 2, 3], 'b': [4, 5]} returns "
        "{'a': 6, 'b': 9}.",
        "def group_totals(groups):\n"
        "    result = {}\n"
        "    for key in groups:\n        result[key] = sum(groups[key])\n"
        "    return result\n",
        [[{"a": [1, 2, 3], "b": [4, 5]}], [{"x": []}], [{"m": [10], "n": [20, 30]}]],
        "",
    ),
    (
        "nested_018", "count_items_per_category",
        "Given a dictionary mapping each category to a list of items, return "
        "a new dictionary mapping each category to how many items it has. "
        "e.g. catalog={'fruits': ['apple', 'banana'], 'veggies': ['carrot']} "
        "returns {'fruits': 2, 'veggies': 1}.",
        "def count_items_per_category(catalog):\n"
        "    result = {}\n"
        "    for key in catalog:\n        result[key] = len(catalog[key])\n"
        "    return result\n",
        [
            [{"fruits": ["apple", "banana"], "veggies": ["carrot"]}],
            [{"x": []}],
            [{"a": [1, 2, 3, 4], "b": [1]}],
        ],
        "",
    ),
    (
        "nested_019", "find_student_with_max_score",
        "Given a list of student dictionaries, return the name of the "
        "student with the highest score. "
        "e.g. students=[{'name': 'Ana', 'score': 90}, {'name': 'Leo', "
        "'score': 95}] returns 'Leo'.",
        "def find_student_with_max_score(students):\n"
        "    best = students[0]\n"
        "    for s in students:\n"
        "        if s['score'] > best['score']:\n            best = s\n"
        "    return best['name']\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 95}]],
            [[{"name": "Sam", "score": 70}]],
            [[{"name": "Al", "score": 50}, {"name": "Kim", "score": 80}, {"name": "Jo", "score": 60}]],
        ],
        "",
    ),
    (
        "nested_020", "list_of_pairs_to_dict",
        "Given a list of (key, value) tuples, return a dictionary built from "
        "them. e.g. pairs=[('a', 1), ('b', 2)] returns {'a': 1, 'b': 2}.",
        "def list_of_pairs_to_dict(pairs):\n"
        "    result = {}\n"
        "    for key, value in pairs:\n        result[key] = value\n"
        "    return result\n",
        [[[("a", 1), ("b", 2)]], [[("x", 10)]], [[("m", 1), ("n", 2), ("o", 3)]]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "nested_debug_001", "sum_of_grid",
        "Given a 2D grid, this function is supposed to return the sum of "
        "every value in it — but it has a bug. Find it and fix it.",
        "def sum_of_grid(grid):\n"
        "    total = 0\n"
        "    for row in grid:\n"
        "        for val in row:\n            total += val\n"
        "    return total\n",
        "def sum_of_grid(grid):\n"
        "    total = 0\n"
        "    for row in grid:\n        total += row[0]\n"
        "    return total\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 2, 3], [4, 5, 6]]]],
    ),
    (
        "nested_debug_002", "transpose_grid",
        "Given a 2D grid, this function is supposed to return it transposed "
        "— but it has a bug. Find it and fix it.",
        "def transpose_grid(grid):\n"
        "    result = []\n"
        "    for col in range(len(grid[0])):\n"
        "        new_row = []\n"
        "        for row in grid:\n            new_row.append(row[col])\n"
        "        result.append(new_row)\n"
        "    return result\n",
        "def transpose_grid(grid):\n"
        "    result = []\n"
        "    for col in range(len(grid)):\n"
        "        new_row = []\n"
        "        for row in grid:\n            new_row.append(row[col])\n"
        "        result.append(new_row)\n"
        "    return result\n",
        [[[[1, 2], [3, 4]]], [[[1, 2, 3]]], [[[1], [2], [3]]]],
    ),
    (
        "nested_debug_003", "filter_students_by_min_score",
        "Given a list of student dictionaries and a min_score, this function "
        "is supposed to return the names of every student whose score is at "
        "least min_score — but it has a bug. Find it and fix it.",
        "def filter_students_by_min_score(students, min_score):\n"
        "    result = []\n"
        "    for s in students:\n"
        "        if s['score'] >= min_score:\n            result.append(s['name'])\n"
        "    return result\n",
        "def filter_students_by_min_score(students, min_score):\n"
        "    result = []\n"
        "    for s in students:\n"
        "        if s['score'] > min_score:\n            result.append(s['name'])\n"
        "    return result\n",
        [
            [[{"name": "Ana", "score": 90}, {"name": "Leo", "score": 60}], 70],
            [[{"name": "Sam", "score": 50}], 70],
            [[{"name": "Al", "score": 95}, {"name": "Kim", "score": 95}], 95],
        ],
    ),
    (
        "nested_debug_004", "diagonal_sum",
        "Given a square 2D grid, this function is supposed to return the sum "
        "of its main diagonal — but it has a bug. Find it and fix it.",
        "def diagonal_sum(grid):\n"
        "    total = 0\n"
        "    for i in range(len(grid)):\n        total += grid[i][i]\n"
        "    return total\n",
        "def diagonal_sum(grid):\n"
        "    total = 0\n"
        "    for i in range(len(grid)):\n        total += grid[i][0]\n"
        "    return total\n",
        [[[[1, 2], [3, 4]]], [[[5]]], [[[1, 0, 0], [0, 2, 0], [0, 0, 3]]]],
    ),
]


def main():
    """Writes all 24 Nested problem files and reports what it did."""
    written = write_topic("nested", "10_nested", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
