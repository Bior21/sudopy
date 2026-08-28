"""One-time authoring script: writes the redesigned Tuples topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.

Several problems below pass real Python tuples in args_list (e.g.
(3, 4) rather than [3, 4]) - write_topic()'s _encode_tuples marks these
so they round-trip through JSON as tuples, not lists, and problem_loader's
_decode_tuples restores them on load. That's what makes a call site show
authentic "(3, 4)" tuple syntax instead of "[3, 4]" list syntax.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "tuples_001", "unpack_pair",
        "Given a 2-element tuple pair, unpack it into two variables and "
        "return their sum. e.g. pair=(3, 4) returns 7.",
        "def unpack_pair(pair):\n    a, b = pair\n    return a + b\n",
        [[(3, 4)], [(10, 20)], [(-5, 5)]],
        "",
    ),
    (
        "tuples_002", "get_element_at",
        "Given a tuple t and an index, return the element at that index. "
        "e.g. t=(10, 20, 30), index=1 returns 20.",
        "def get_element_at(t, index):\n    return t[index]\n",
        [[(10, 20, 30), 1], [(5,), 0], [(1, 2, 3, 4), 3]],
        "",
    ),
    (
        "tuples_003", "tuple_length",
        "Given a tuple t, return how many elements it has. "
        "e.g. t=(1, 2, 3) returns 3.",
        "def tuple_length(t):\n    return len(t)\n",
        [[(1, 2, 3)], [()], [(1, 2, 3, 4, 5)]],
        "",
    ),
    (
        "tuples_004", "swap_pair",
        "Given a 2-element tuple pair, return a new tuple with the two "
        "elements swapped. e.g. pair=(1, 2) returns (2, 1).",
        "def swap_pair(pair):\n    a, b = pair\n    return b, a\n",
        [[(1, 2)], [(5, 10)], [(0, -3)]],
        "",
    ),
    (
        "tuples_005", "make_point",
        "Given an x and a y, return them packed together as a tuple. "
        "e.g. x=3, y=4 returns (3, 4).",
        "def make_point(x, y):\n    return (x, y)\n",
        [[3, 4], [0, 0], [-1, 5]],
        "",
    ),
    (
        "tuples_006", "distance_squared_between_points",
        "Given two points, each an (x, y) tuple, return the squared "
        "distance between them (skip the square root). "
        "e.g. p1=(0, 0), p2=(3, 4) returns 25.",
        "def distance_squared_between_points(p1, p2):\n"
        "    x1, y1 = p1\n"
        "    x2, y2 = p2\n"
        "    return (x2 - x1) ** 2 + (y2 - y1) ** 2\n",
        [[(0, 0), (3, 4)], [(1, 1), (1, 1)], [(0, 0), (1, 1)]],
        "",
    ),
    (
        "tuples_007", "tuple_to_list",
        "Given a tuple t, return it converted to a list. "
        "e.g. t=(1, 2, 3) returns [1, 2, 3].",
        "def tuple_to_list(t):\n    return list(t)\n",
        [[(1, 2, 3)], [()], [(5,)]],
        "",
    ),
    (
        "tuples_008", "list_to_tuple",
        "Given a list lst, return it converted to a tuple. "
        "e.g. lst=[1, 2, 3] returns (1, 2, 3).",
        "def list_to_tuple(lst):\n    return tuple(lst)\n",
        [[[1, 2, 3]], [[]], [[5]]],
        "",
    ),
    (
        "tuples_009", "concatenate_tuples",
        "Given two tuples a and b, return them joined into one tuple, a's "
        "elements first. e.g. a=(1, 2), b=(3, 4) returns (1, 2, 3, 4).",
        "def concatenate_tuples(a, b):\n    return a + b\n",
        [[(1, 2), (3, 4)], [(), (1, 2)], [(5,), ()]],
        "",
    ),
    (
        "tuples_010", "count_value_in_tuple",
        "Given a tuple t and a value, return how many times value appears "
        "in t. e.g. t=(1, 2, 2, 3, 2), value=2 returns 3.",
        "def count_value_in_tuple(t, value):\n    return t.count(value)\n",
        [[(1, 2, 2, 3, 2), 2], [(1, 2, 3), 5], [(4, 4, 4), 4]],
        "",
    ),
    (
        "tuples_011", "index_of_value_in_tuple",
        "Given a tuple t and a value known to be in it, return the index "
        "where value first appears. e.g. t=(10, 20, 30), value=20 returns 1.",
        "def index_of_value_in_tuple(t, value):\n    return t.index(value)\n",
        [[(10, 20, 30), 20], [(5, 6, 7), 5], [(1, 2, 3), 3]],
        "",
    ),
    (
        "tuples_012", "first_and_last",
        "Given a tuple t, return a new 2-element tuple made of its first and "
        "last elements. e.g. t=(1, 2, 3, 4) returns (1, 4).",
        "def first_and_last(t):\n    return (t[0], t[-1])\n",
        [[(1, 2, 3, 4)], [(7,)], [(9, 5)]],
        "",
    ),
    (
        "tuples_013", "slice_tuple",
        "Given a tuple t and a start/end index, return the slice t[start:end]. "
        "e.g. t=(1, 2, 3, 4, 5), start=1, end=3 returns (2, 3).",
        "def slice_tuple(t, start, end):\n    return t[start:end]\n",
        [[(1, 2, 3, 4, 5), 1, 3], [(1, 2, 3), 0, 2], [(1, 2, 3), 0, 10]],
        "",
    ),
    (
        "tuples_014", "sum_of_tuple",
        "Given a tuple of numbers, return their sum. "
        "e.g. t=(1, 2, 3) returns 6.",
        "def sum_of_tuple(t):\n    return sum(t)\n",
        [[(1, 2, 3)], [()], [(10,)]],
        "",
    ),
    (
        "tuples_015", "max_of_tuple",
        "Given a tuple of numbers, return the largest one. "
        "e.g. t=(3, 1, 4, 1, 5) returns 5.",
        "def max_of_tuple(t):\n    return max(t)\n",
        [[(3, 1, 4, 1, 5)], [(-5, -2, -10)], [(7,)]],
        "",
    ),
    (
        "tuples_016", "pairs_from_two_lists",
        "Given two same-length lists a and b, return a list of tuples "
        "pairing up the elements at each position. "
        "e.g. a=[1, 2, 3], b=['x', 'y', 'z'] returns [(1, 'x'), (2, 'y'), (3, 'z')].",
        "def pairs_from_two_lists(a, b):\n    return list(zip(a, b))\n",
        [[[1, 2, 3], ["x", "y", "z"]], [[1], [10]], [[], []]],
        "zip() pairs up two sequences elementwise into tuples - wrap it in list() to see the pairs.",
    ),
    (
        "tuples_017", "sum_of_pairs",
        "Given a list of 2-element tuples, return a list with the sum of "
        "each pair, in order. e.g. pairs=[(1, 2), (3, 4)] returns [3, 7].",
        "def sum_of_pairs(pairs):\n"
        "    result = []\n"
        "    for a, b in pairs:\n        result.append(a + b)\n"
        "    return result\n",
        [[[(1, 2), (3, 4)]], [[(0, 0)]], [[(5, 5), (10, -10)]]],
        "You can unpack each tuple right in the for loop header: for a, b in pairs.",
    ),
    (
        "tuples_018", "swap_first_last",
        "Given a tuple t with at least two elements, return a new tuple with "
        "its first and last elements swapped and everything in between "
        "unchanged. e.g. t=(1, 2, 3, 4) returns (4, 2, 3, 1).",
        "def swap_first_last(t):\n"
        "    t_list = list(t)\n"
        "    t_list[0], t_list[-1] = t_list[-1], t_list[0]\n"
        "    return tuple(t_list)\n",
        [[(1, 2, 3, 4)], [(1, 2)], [(9, 5, 1)]],
        "Tuples can't be modified directly - convert to a list, swap there, then convert back.",
    ),
    (
        "tuples_019", "tuples_are_equal",
        "Given two tuples a and b, return whether they contain the same "
        "elements in the same order. "
        "e.g. a=(1, 2, 3), b=(1, 2, 3) returns True.",
        "def tuples_are_equal(a, b):\n    return a == b\n",
        [[(1, 2, 3), (1, 2, 3)], [(1, 2, 3), (3, 2, 1)], [(1, 2), (1, 2, 3)]],
        "",
    ),
    (
        "tuples_020", "sort_tuples_by_second",
        "Given a list of 2-element tuples, return it sorted by each tuple's "
        "second element, smallest first. "
        "e.g. pairs=[('a', 3), ('b', 1), ('c', 2)] returns "
        "[('b', 1), ('c', 2), ('a', 3)].",
        "def sort_tuples_by_second(pairs):\n"
        "    return sorted(pairs, key=lambda p: p[1])\n",
        [
            [[("a", 3), ("b", 1), ("c", 2)]],
            [[("x", 1)]],
            [[("a", 5), ("b", 5), ("c", 1)]],
        ],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "tuples_debug_001", "swap_pair",
        "Given a 2-element tuple pair, this function is supposed to return a "
        "new tuple with the two elements swapped — but it has a bug. "
        "Find it and fix it.",
        "def swap_pair(pair):\n    a, b = pair\n    return b, a\n",
        "def swap_pair(pair):\n    a, b = pair\n    return a, b\n",
        [[(1, 2)], [(5, 10)], [(0, -3)]],
    ),
    (
        "tuples_debug_002", "concatenate_tuples",
        "Given two tuples a and b, this function is supposed to return them "
        "joined into one tuple, a's elements first — but it has a bug. "
        "Find it and fix it.",
        "def concatenate_tuples(a, b):\n    return a + b\n",
        "def concatenate_tuples(a, b):\n    return b + a\n",
        [[(1, 2), (3, 4)], [(), (1, 2)], [(5,), ()]],
    ),
    (
        "tuples_debug_003", "first_and_last",
        "Given a tuple t, this function is supposed to return a new "
        "2-element tuple made of its first and last elements — but it has a "
        "bug. Find it and fix it.",
        "def first_and_last(t):\n    return (t[0], t[-1])\n",
        "def first_and_last(t):\n    return (t[0], t[0])\n",
        [[(1, 2, 3, 4)], [(7,)], [(9, 5)]],
    ),
    (
        "tuples_debug_004", "sum_of_pairs",
        "Given a list of 2-element tuples, this function is supposed to "
        "return a list with the sum of each pair, in order — but it has a "
        "bug. Find it and fix it.",
        "def sum_of_pairs(pairs):\n"
        "    result = []\n"
        "    for a, b in pairs:\n        result.append(a + b)\n"
        "    return result\n",
        "def sum_of_pairs(pairs):\n"
        "    result = []\n"
        "    for a, b in pairs:\n        result.append(a)\n"
        "    return result\n",
        [[[(1, 2), (3, 4)]], [[(0, 0)]], [[(5, 5), (10, -10)]]],
    ),
]


def main():
    """Writes all 24 Tuples problem files and reports what it did."""
    written = write_topic("tuples", "09_tuples", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
