"""One-time authoring script: writes the redesigned Lists topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "lists_001", "sum_of_list",
        "Given a list of numbers, return their sum. e.g. nums=[1, 2, 3] returns 6.",
        "def sum_of_list(nums):\n    return sum(nums)\n",
        [[[1, 2, 3]], [[10, 20, 30, 40]], [[5]]],
        "",
    ),
    (
        "lists_002", "average_of_list",
        "Given a list of numbers, return their average. "
        "e.g. nums=[10, 20, 30] returns 20.0.",
        "def average_of_list(nums):\n    return sum(nums) / len(nums)\n",
        [[[10, 20, 30]], [[4, 4, 4, 4]], [[7]]],
        "",
    ),
    (
        "lists_003", "find_maximum",
        "Given a list of numbers, return the largest one. "
        "e.g. nums=[3, 1, 4, 1, 5, 9] returns 9.",
        "def find_maximum(nums):\n    return max(nums)\n",
        [[[3, 1, 4, 1, 5, 9]], [[-5, -2, -10]], [[7]]],
        "",
    ),
    (
        "lists_004", "find_minimum",
        "Given a list of numbers, return the smallest one. "
        "e.g. nums=[3, 1, 4, 1, 5, 9] returns 1.",
        "def find_minimum(nums):\n    return min(nums)\n",
        [[[3, 1, 4, 1, 5, 9]], [[-5, -2, -10]], [[7]]],
        "",
    ),
    (
        "lists_005", "count_occurrences",
        "Given a list of numbers and a target, return how many times target "
        "appears in nums. e.g. nums=[1, 2, 2, 3, 2], target=2 returns 3.",
        "def count_occurrences(nums, target):\n    return nums.count(target)\n",
        [[[1, 2, 2, 3, 2], 2], [[1, 2, 3], 5], [[4, 4, 4], 4]],
        "",
    ),
    (
        "lists_006", "contains_value",
        "Given a list of numbers and a target, return whether target appears "
        "in nums. e.g. nums=[1, 2, 3], target=2 returns True.",
        "def contains_value(nums, target):\n    return target in nums\n",
        [[[1, 2, 3], 2], [[1, 2, 3], 5], [[], 1]],
        "",
    ),
    (
        "lists_007", "index_of_value",
        "Given a list of numbers and a target known to be in it, return the "
        "index where target first appears. "
        "e.g. nums=[10, 20, 30], target=20 returns 1.",
        "def index_of_value(nums, target):\n    return nums.index(target)\n",
        [[[10, 20, 30], 20], [[5, 6, 7], 5], [[1, 2, 3], 3]],
        "",
    ),
    (
        "lists_008", "reverse_list",
        "Given a list of numbers, return it reversed. "
        "e.g. nums=[1, 2, 3] returns [3, 2, 1].",
        "def reverse_list(nums):\n    return nums[::-1]\n",
        [[[1, 2, 3]], [[5]], [[4, 3, 2, 1]]],
        "",
    ),
    (
        "lists_009", "first_n_elements",
        "Given a list of numbers and a count n, return its first n elements. "
        "e.g. nums=[1, 2, 3, 4, 5], n=3 returns [1, 2, 3].",
        "def first_n_elements(nums, n):\n    return nums[:n]\n",
        [[[1, 2, 3, 4, 5], 3], [[1, 2, 3], 5], [[1, 2, 3], 0]],
        "",
    ),
    (
        "lists_010", "last_n_elements",
        "Given a list of numbers and a count n, return its last n elements. "
        "e.g. nums=[1, 2, 3, 4, 5], n=2 returns [4, 5].",
        "def last_n_elements(nums, n):\n    return nums[-n:]\n",
        [[[1, 2, 3, 4, 5], 2], [[1, 2, 3], 5], [[1, 2, 3], 1]],
        "",
    ),
    (
        "lists_011", "append_value",
        "Given a list of numbers and a value, append value to the end of nums "
        "and return nums. e.g. nums=[1, 2, 3], value=4 returns [1, 2, 3, 4].",
        "def append_value(nums, value):\n    nums.append(value)\n    return nums\n",
        [[[1, 2, 3], 4], [[], 1], [[5], 10]],
        "",
    ),
    (
        "lists_012", "remove_value",
        "Given a list of numbers and a value known to be in it, remove the "
        "first occurrence of value from nums and return nums. "
        "e.g. nums=[1, 2, 3], value=2 returns [1, 3].",
        "def remove_value(nums, value):\n    nums.remove(value)\n    return nums\n",
        [[[1, 2, 3], 2], [[5, 6, 7], 5], [[1, 1, 2], 1]],
        "remove() only takes out the first match — with nums=[1, 1, 2], value=1, one 1 stays behind.",
    ),
    (
        "lists_013", "double_each_element",
        "Given a list of numbers, return a new list where every number is "
        "doubled. e.g. nums=[1, 2, 3] returns [2, 4, 6].",
        "def double_each_element(nums):\n"
        "    result = []\n"
        "    for n in nums:\n        result.append(n * 2)\n"
        "    return result\n",
        [[[1, 2, 3]], [[0, 5, 10]], [[-1, -2]]],
        "",
    ),
    (
        "lists_014", "filter_evens",
        "Given a list of numbers, return a new list with only the even ones, "
        "in the same order. e.g. nums=[1, 2, 3, 4, 5, 6] returns [2, 4, 6].",
        "def filter_evens(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n % 2 == 0:\n            result.append(n)\n"
        "    return result\n",
        [[[1, 2, 3, 4, 5, 6]], [[1, 3, 5]], [[2, 4, 6]]],
        "",
    ),
    (
        "lists_015", "filter_greater_than",
        "Given a list of numbers and a threshold, return a new list with only "
        "the numbers strictly greater than threshold. "
        "e.g. nums=[1, 5, 10, 15, 20], threshold=10 returns [15, 20].",
        "def filter_greater_than(nums, threshold):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n > threshold:\n            result.append(n)\n"
        "    return result\n",
        [[[1, 5, 10, 15, 20], 10], [[1, 2, 3], 10], [[5, 5, 5], 5]],
        "",
    ),
    (
        "lists_016", "count_positive",
        "Given a list of numbers, return how many of them are positive. "
        "e.g. nums=[1, -2, 3, -4, 5] returns 3.",
        "def count_positive(nums):\n"
        "    count = 0\n"
        "    for n in nums:\n"
        "        if n > 0:\n            count += 1\n"
        "    return count\n",
        [[[1, -2, 3, -4, 5]], [[-1, -2, -3]], [[1, 2, 3]]],
        "",
    ),
    (
        "lists_017", "squares_of_list",
        "Given a list of numbers, return a new list with each number squared. "
        "e.g. nums=[1, 2, 3] returns [1, 4, 9].",
        "def squares_of_list(nums):\n"
        "    result = []\n"
        "    for n in nums:\n        result.append(n * n)\n"
        "    return result\n",
        [[[1, 2, 3]], [[0, 5]], [[-2, -3]]],
        "",
    ),
    (
        "lists_018", "merge_two_lists",
        "Given two lists a and b, return a single list with all of a's "
        "elements followed by all of b's. e.g. a=[1, 2], b=[3, 4] returns "
        "[1, 2, 3, 4].",
        "def merge_two_lists(a, b):\n    return a + b\n",
        [[[1, 2], [3, 4]], [[], [1, 2]], [[5], []]],
        "",
    ),
    (
        "lists_019", "remove_duplicates",
        "Given a list of numbers, return a new list with duplicates removed, "
        "keeping only each number's first appearance and preserving order. "
        "e.g. nums=[1, 2, 2, 3, 1, 4] returns [1, 2, 3, 4].",
        "def remove_duplicates(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n not in result:\n            result.append(n)\n"
        "    return result\n",
        [[[1, 2, 2, 3, 1, 4]], [[5, 5, 5]], [[1, 2, 3]]],
        "",
    ),
    (
        "lists_020", "second_largest",
        "Given a list of at least two numbers, return the second largest "
        "value. e.g. nums=[3, 1, 4, 1, 5, 9, 2, 6] returns 6.",
        "def second_largest(nums):\n"
        "    first = max(nums[0], nums[1])\n"
        "    second = min(nums[0], nums[1])\n"
        "    for n in nums[2:]:\n"
        "        if n > first:\n"
        "            second = first\n"
        "            first = n\n"
        "        elif n > second:\n"
        "            second = n\n"
        "    return second\n",
        [[[1, 2, 3, 4, 5]], [[10, 20]], [[5, 5, 9]]],
        "Track both the largest and second largest as you scan — when a new number beats the largest, the old largest becomes the new second largest.",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "lists_debug_001", "find_maximum",
        "Given a list of numbers, this function is supposed to return the "
        "largest one — but it has a bug. Find it and fix it.",
        "def find_maximum(nums):\n    return max(nums)\n",
        "def find_maximum(nums):\n"
        "    max_val = 0\n"
        "    for n in nums:\n"
        "        if n > max_val:\n            max_val = n\n"
        "    return max_val\n",
        [[[3, 1, 4, 1, 5, 9]], [[-5, -2, -10]], [[7]]],
    ),
    (
        "lists_debug_002", "filter_evens",
        "Given a list of numbers, this function is supposed to return a new "
        "list with only the even ones — but it has a bug. Find it and fix it.",
        "def filter_evens(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n % 2 == 0:\n            result.append(n)\n"
        "    return result\n",
        "def filter_evens(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n % 2 == 1:\n            result.append(n)\n"
        "    return result\n",
        [[[1, 2, 3, 4, 5, 6]], [[1, 3, 5]], [[2, 4, 6]]],
    ),
    (
        "lists_debug_003", "remove_duplicates",
        "Given a list of numbers, this function is supposed to return a new "
        "list with duplicates removed — but it has a bug. Find it and fix it.",
        "def remove_duplicates(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n not in result:\n            result.append(n)\n"
        "    return result\n",
        "def remove_duplicates(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        result.append(n)\n"
        "    return result\n",
        [[[1, 2, 2, 3, 1, 4]], [[5, 5, 5]], [[1, 2, 3]]],
    ),
    (
        "lists_debug_004", "second_largest",
        "Given a list of at least two numbers, this function is supposed to "
        "return the second largest value — but it has a bug. "
        "Find it and fix it.",
        "def second_largest(nums):\n"
        "    first = max(nums[0], nums[1])\n"
        "    second = min(nums[0], nums[1])\n"
        "    for n in nums[2:]:\n"
        "        if n > first:\n"
        "            second = first\n"
        "            first = n\n"
        "        elif n > second:\n"
        "            second = n\n"
        "    return second\n",
        "def second_largest(nums):\n"
        "    first = max(nums[0], nums[1])\n"
        "    second = min(nums[0], nums[1])\n"
        "    for n in nums[2:]:\n"
        "        if n > first:\n"
        "            first = n\n"
        "        elif n > second:\n"
        "            second = n\n"
        "    return second\n",
        [[[1, 2, 3, 4, 5]], [[10, 20]], [[5, 5, 9]]],
    ),
]


def main():
    """Writes all 24 Lists problem files and reports what it did."""
    written = write_topic("lists", "07_lists", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
