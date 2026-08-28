"""One-time authoring script: writes the redesigned Dictionaries topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "dictionaries_001", "get_value",
        "Given a dictionary d and a key known to be in it, return the value "
        "stored at that key. e.g. d={'sam': 12, 'al': 15}, key='al' returns 15.",
        "def get_value(d, key):\n    return d[key]\n",
        [[{"sam": 12, "al": 15}, "al"], [{"math": 90, "art": 85}, "math"], [{"x": 1}, "x"]],
        "",
    ),
    (
        "dictionaries_002", "has_key",
        "Given a dictionary d and a key, return whether key is in d. "
        "e.g. d={'a': 1, 'b': 2}, key='a' returns True.",
        "def has_key(d, key):\n    return key in d\n",
        [[{"a": 1, "b": 2}, "a"], [{"a": 1}, "c"], [{}, "z"]],
        "",
    ),
    (
        "dictionaries_003", "add_or_update",
        "Given a dictionary d, a key, and a value, set d[key] to value (adding "
        "it if new, overwriting it if not) and return d. "
        "e.g. d={'a': 1}, key='b', value=2 returns {'a': 1, 'b': 2}.",
        "def add_or_update(d, key, value):\n    d[key] = value\n    return d\n",
        [[{"a": 1}, "b", 2], [{"a": 1}, "a", 99], [{}, "x", 5]],
        "",
    ),
    (
        "dictionaries_004", "remove_key",
        "Given a dictionary d and a key known to be in it, remove that key "
        "from d and return d. e.g. d={'a': 1, 'b': 2}, key='a' returns {'b': 2}.",
        "def remove_key(d, key):\n    del d[key]\n    return d\n",
        [[{"a": 1, "b": 2}, "a"], [{"x": 1}, "x"], [{"a": 1, "b": 2, "c": 3}, "b"]],
        "",
    ),
    (
        "dictionaries_005", "count_keys",
        "Given a dictionary d, return how many keys it has. "
        "e.g. d={'a': 1, 'b': 2} returns 2.",
        "def count_keys(d):\n    return len(d)\n",
        [[{"a": 1, "b": 2}], [{}], [{"x": 1, "y": 2, "z": 3}]],
        "",
    ),
    (
        "dictionaries_006", "get_with_default",
        "Given a dictionary d, a key, and a default, return d's value at key "
        "if key is in d, or default otherwise. "
        "e.g. d={'a': 1}, key='b', default=0 returns 0.",
        "def get_with_default(d, key, default):\n    return d.get(key, default)\n",
        [[{"a": 1}, "a", 0], [{"a": 1}, "b", 0], [{}, "z", -1]],
        "",
    ),
    (
        "dictionaries_007", "all_keys",
        "Given a dictionary d, return a list of all its keys. "
        "e.g. d={'a': 1, 'b': 2} returns ['a', 'b'].",
        "def all_keys(d):\n    return list(d.keys())\n",
        [[{"a": 1, "b": 2}], [{}], [{"x": 1}]],
        "",
    ),
    (
        "dictionaries_008", "all_values",
        "Given a dictionary d, return a list of all its values. "
        "e.g. d={'a': 1, 'b': 2} returns [1, 2].",
        "def all_values(d):\n    return list(d.values())\n",
        [[{"a": 1, "b": 2}], [{}], [{"x": 5, "y": 10}]],
        "",
    ),
    (
        "dictionaries_009", "sum_of_values",
        "Given a dictionary d whose values are numbers, return their sum. "
        "e.g. d={'a': 1, 'b': 2, 'c': 3} returns 6.",
        "def sum_of_values(d):\n    return sum(d.values())\n",
        [[{"a": 1, "b": 2, "c": 3}], [{}], [{"x": 10}]],
        "",
    ),
    (
        "dictionaries_010", "max_value_key",
        "Given a dictionary d whose values are numbers, return the key with "
        "the largest value. e.g. d={'a': 3, 'b': 7, 'c': 2} returns 'b'.",
        "def max_value_key(d):\n    return max(d, key=d.get)\n",
        [[{"a": 3, "b": 7, "c": 2}], [{"x": 1}], [{"m": 5, "n": 9, "o": 1}]],
        "",
    ),
    (
        "dictionaries_011", "count_word_frequencies",
        "Given a list of words, return a dictionary mapping each word to how "
        "many times it appears. "
        "e.g. words=['a', 'b', 'a', 'c', 'b', 'a'] returns {'a': 3, 'b': 2, 'c': 1}.",
        "def count_word_frequencies(words):\n"
        "    freq = {}\n"
        "    for word in words:\n"
        "        freq[word] = freq.get(word, 0) + 1\n"
        "    return freq\n",
        [[["a", "b", "a", "c", "b", "a"]], [["x"]], [["hi", "hi", "hi"]]],
        "",
    ),
    (
        "dictionaries_012", "merge_dicts",
        "Given two dictionaries a and b, return a new dictionary with all of "
        "a's pairs plus all of b's - where a key is in both, b's value wins. "
        "e.g. a={'a': 1, 'b': 2}, b={'b': 20, 'c': 3} returns "
        "{'a': 1, 'b': 20, 'c': 3}.",
        "def merge_dicts(a, b):\n"
        "    result = dict(a)\n"
        "    for key in b:\n        result[key] = b[key]\n"
        "    return result\n",
        [[{"a": 1, "b": 2}, {"b": 20, "c": 3}], [{}, {"x": 1}], [{"a": 1}, {}]],
        "",
    ),
    (
        "dictionaries_013", "invert_dict",
        "Given a dictionary d whose values are unique, return a new "
        "dictionary with keys and values swapped. "
        "e.g. d={'a': 1, 'b': 2} returns {1: 'a', 2: 'b'}.",
        "def invert_dict(d):\n"
        "    result = {}\n"
        "    for key in d:\n        result[d[key]] = key\n"
        "    return result\n",
        [[{"a": 1, "b": 2, "c": 3}], [{"x": 10}], [{"p": 1, "q": 2}]],
        "",
    ),
    (
        "dictionaries_014", "filter_by_value_threshold",
        "Given a dictionary d whose values are numbers and a threshold, "
        "return a new dictionary with only the pairs whose value is strictly "
        "greater than threshold. e.g. d={'a': 5, 'b': 15, 'c': 25}, "
        "threshold=10 returns {'b': 15, 'c': 25}.",
        "def filter_by_value_threshold(d, threshold):\n"
        "    result = {}\n"
        "    for key in d:\n"
        "        if d[key] > threshold:\n            result[key] = d[key]\n"
        "    return result\n",
        [[{"a": 5, "b": 15, "c": 25}, 10], [{"x": 1, "y": 2}, 10], [{"m": 100}, 50]],
        "",
    ),
    (
        "dictionaries_015", "increment_value",
        "Given a dictionary d whose values are numbers and a key known to be "
        "in it, add 1 to the value at that key and return d. "
        "e.g. d={'a': 1, 'b': 2}, key='a' returns {'a': 2, 'b': 2}.",
        "def increment_value(d, key):\n    d[key] += 1\n    return d\n",
        [[{"a": 1, "b": 2}, "a"], [{"x": 9}, "x"], [{"a": 1, "b": 2}, "b"]],
        "",
    ),
    (
        "dictionaries_016", "keys_with_value",
        "Given a dictionary d and a target_value, return a list of every key "
        "whose value equals target_value. "
        "e.g. d={'a': 1, 'b': 2, 'c': 1}, target_value=1 returns ['a', 'c'].",
        "def keys_with_value(d, target_value):\n"
        "    result = []\n"
        "    for key in d:\n"
        "        if d[key] == target_value:\n            result.append(key)\n"
        "    return result\n",
        [[{"a": 1, "b": 2, "c": 1}, 1], [{"x": 5}, 9], [{"m": 3, "n": 3, "o": 3}, 3]],
        "",
    ),
    (
        "dictionaries_017", "average_of_values",
        "Given a dictionary d whose values are numbers, return their average. "
        "e.g. d={'a': 10, 'b': 20, 'c': 30} returns 20.0.",
        "def average_of_values(d):\n    return sum(d.values()) / len(d)\n",
        [[{"a": 10, "b": 20, "c": 30}], [{"x": 5}], [{"a": 4, "b": 4, "c": 4, "d": 4}]],
        "",
    ),
    (
        "dictionaries_018", "combine_counts",
        "Given a dictionary d of running counts, a key, and an amount, add "
        "amount to d's count for key - treating a missing key as starting at "
        "0 - and return d. e.g. d={'a': 5}, key='b', amount=2 returns "
        "{'a': 5, 'b': 2}.",
        "def combine_counts(d, key, amount):\n"
        "    d[key] = d.get(key, 0) + amount\n"
        "    return d\n",
        [[{"a": 5}, "a", 3], [{"a": 5}, "b", 2], [{}, "x", 7]],
        "",
    ),
    (
        "dictionaries_019", "dict_from_two_lists",
        "Given a list of keys and a same-length list of values, return a "
        "dictionary pairing each key with the value at the same position. "
        "e.g. keys=['a', 'b', 'c'], values=[1, 2, 3] returns "
        "{'a': 1, 'b': 2, 'c': 3}.",
        "def dict_from_two_lists(keys, values):\n"
        "    result = {}\n"
        "    for i in range(len(keys)):\n        result[keys[i]] = values[i]\n"
        "    return result\n",
        [[["a", "b", "c"], [1, 2, 3]], [["x"], [10]], [[], []]],
        "",
    ),
    (
        "dictionaries_020", "count_matching_values",
        "Given a dictionary d and a target, return how many of its values "
        "equal target. e.g. d={'a': 1, 'b': 2, 'c': 1, 'd': 1}, target=1 "
        "returns 3.",
        "def count_matching_values(d, target):\n"
        "    count = 0\n"
        "    for key in d:\n"
        "        if d[key] == target:\n            count += 1\n"
        "    return count\n",
        [[{"a": 1, "b": 2, "c": 1, "d": 1}, 1], [{"x": 5}, 9], [{"m": 3, "n": 3}, 3]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "dictionaries_debug_001", "get_with_default",
        "Given d, a key, and a default, this function is supposed to return "
        "d's value at key, or default if key isn't in d — but it has a bug. "
        "Find it and fix it.",
        "def get_with_default(d, key, default):\n    return d.get(key, default)\n",
        "def get_with_default(d, key, default):\n    return d.get(key)\n",
        [[{"a": 1}, "a", 0], [{"a": 1}, "b", 0], [{}, "z", -1]],
    ),
    (
        "dictionaries_debug_002", "merge_dicts",
        "Given two dictionaries a and b, this function is supposed to return "
        "a new dictionary with all of a's pairs plus all of b's — but it has "
        "a bug. Find it and fix it.",
        "def merge_dicts(a, b):\n"
        "    result = dict(a)\n"
        "    for key in b:\n        result[key] = b[key]\n"
        "    return result\n",
        "def merge_dicts(a, b):\n    return dict(a)\n",
        [[{"a": 1, "b": 2}, {"b": 20, "c": 3}], [{}, {"x": 1}], [{"a": 1}, {}]],
    ),
    (
        "dictionaries_debug_003", "invert_dict",
        "Given a dictionary d whose values are unique, this function is "
        "supposed to return a new dictionary with keys and values swapped — "
        "but it has a bug. Find it and fix it.",
        "def invert_dict(d):\n"
        "    result = {}\n"
        "    for key in d:\n        result[d[key]] = key\n"
        "    return result\n",
        "def invert_dict(d):\n"
        "    result = {}\n"
        "    for key in d:\n        result[key] = d[key]\n"
        "    return result\n",
        [[{"a": 1, "b": 2, "c": 3}], [{"x": 10}], [{"p": 1, "q": 2}]],
    ),
    (
        "dictionaries_debug_004", "count_matching_values",
        "Given a dictionary d and a target, this function is supposed to "
        "return how many of its values equal target — but it has a bug. "
        "Find it and fix it.",
        "def count_matching_values(d, target):\n"
        "    count = 0\n"
        "    for key in d:\n"
        "        if d[key] == target:\n            count += 1\n"
        "    return count\n",
        "def count_matching_values(d, target):\n"
        "    count = 0\n"
        "    for key in d:\n"
        "        if key == target:\n            count += 1\n"
        "    return count\n",
        [[{"a": 1, "b": 2, "c": 1, "d": 1}, 1], [{"x": 5}, 9], [{"m": 3, "n": 3}, 3]],
    ),
]


def main():
    """Writes all 24 Dictionaries problem files and reports what it did."""
    written = write_topic("dictionaries", "08_dictionaries", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
