"""One-time authoring script: writes the redesigned Strings topic content.

See write_loops_content.py's docstring for the general pattern; the
actual writing (computing every expected_output for real, confirming
every debug bug genuinely reproduces) is shared logic in
content_authoring.py.
"""

from content_authoring import write_topic

# Each write problem: (id, function_name, prompt, correct_solution, list_of_args, hint)
WRITE_PROBLEMS = [
    (
        "strings_001", "reverse_string",
        "Given a string s, return it reversed. e.g. s='hello' returns 'olleh'.",
        "def reverse_string(s):\n    return s[::-1]\n",
        [["hello"], ["a"], ["racecar"]],
        "",
    ),
    (
        "strings_002", "is_palindrome",
        "Given a string s, return whether it reads the same forwards and "
        "backwards. e.g. s='racecar' returns True; s='hello' returns False.",
        "def is_palindrome(s):\n    return s == s[::-1]\n",
        [["racecar"], ["hello"], ["a"]],
        "",
    ),
    (
        "strings_003", "count_character",
        "Given a string s and a single character ch, return how many times ch "
        "appears in s. e.g. s='banana', ch='a' returns 3.",
        "def count_character(s, ch):\n    return s.count(ch)\n",
        [["banana", "a"], ["hello", "l"], ["xyz", "a"]],
        "",
    ),
    (
        "strings_004", "first_and_last_char",
        "Given a string s, return a new 2-character string made of its first and "
        "last characters. e.g. s='hello' returns 'ho'.",
        "def first_and_last_char(s):\n    return s[0] + s[-1]\n",
        [["hello"], ["ab"], ["x"]],
        "",
    ),
    (
        "strings_005", "remove_spaces",
        "Given a string s, return it with every space removed. "
        "e.g. s='hello world' returns 'helloworld'.",
        "def remove_spaces(s):\n    return s.replace(' ', '')\n",
        [["hello world"], ["a b c"], ["noSpaces"]],
        "",
    ),
    (
        "strings_006", "contains_substring",
        "Given a string s and a substring sub, return whether sub appears "
        "anywhere inside s. e.g. s='hello world', sub='world' returns True.",
        "def contains_substring(s, sub):\n    return sub in s\n",
        [["hello world", "world"], ["hello", "xyz"], ["python", "th"]],
        "",
    ),
    (
        "strings_007", "slice_middle",
        "Given a string s, return it with the first and last characters removed. "
        "e.g. s='hello' returns 'ell'.",
        "def slice_middle(s):\n    return s[1:-1]\n",
        [["hello"], ["ab"], ["python"]],
        "",
    ),
    (
        "strings_008", "count_words",
        "Given a string s of words separated by spaces, return how many words it "
        "has. e.g. s='hello world' returns 2.",
        "def count_words(s):\n    return len(s.split())\n",
        [["hello world"], ["  a   b  c "], ["single"]],
        "",
    ),
    (
        "strings_009", "capitalize_first_letter",
        "Given a non-empty string s, return it with its first letter capitalized. "
        "e.g. s='hello' returns 'Hello'.",
        "def capitalize_first_letter(s):\n    return s[0].upper() + s[1:]\n",
        [["hello"], ["world"], ["a"]],
        "",
    ),
    (
        "strings_010", "replace_character",
        "Given a string s and two characters old and new, return s with every "
        "occurrence of old replaced by new. "
        "e.g. s='hello', old='l', new='L' returns 'heLLo'.",
        "def replace_character(s, old, new):\n    return s.replace(old, new)\n",
        [["hello", "l", "L"], ["banana", "a", "o"], ["test", "x", "y"]],
        "",
    ),
    (
        "strings_011", "starts_with",
        "Given a string s and a prefix, return whether s starts with prefix. "
        "e.g. s='hello world', prefix='hello' returns True.",
        "def starts_with(s, prefix):\n    return s.startswith(prefix)\n",
        [["hello world", "hello"], ["hello", "world"], ["python", "py"]],
        "",
    ),
    (
        "strings_012", "ends_with",
        "Given a string s and a suffix, return whether s ends with suffix. "
        "e.g. s='hello world', suffix='world' returns True.",
        "def ends_with(s, suffix):\n    return s.endswith(suffix)\n",
        [["hello world", "world"], ["hello", "world"], ["python", "on"]],
        "",
    ),
    (
        "strings_013", "join_with_separator",
        "Given a list of words and a separator, return them joined into one "
        "string with separator between each pair. "
        "e.g. words=['a', 'b', 'c'], separator='-' returns 'a-b-c'.",
        "def join_with_separator(words, separator):\n    return separator.join(words)\n",
        [[["a", "b", "c"], "-"], [["hello", "world"], " "], [["x"], ","]],
        "",
    ),
    (
        "strings_014", "split_into_words",
        "Given a string s of words separated by spaces, return a list of the "
        "individual words. e.g. s='hello world' returns ['hello', 'world'].",
        "def split_into_words(s):\n    return s.split()\n",
        [["hello world"], ["a b c"], ["single"]],
        "",
    ),
    (
        "strings_015", "is_all_digits",
        "Given a string s, return whether every character in it is a digit. "
        "e.g. s='12345' returns True; s='12a45' returns False.",
        "def is_all_digits(s):\n    return s.isdigit()\n",
        [["12345"], ["12a45"], ["0"]],
        "",
    ),
    (
        "strings_016", "count_uppercase_letters",
        "Given a string s, return how many of its characters are uppercase "
        "letters. e.g. s='Hello World' returns 2.",
        "def count_uppercase_letters(s):\n"
        "    count = 0\n"
        "    for ch in s:\n"
        "        if ch.isupper():\n            count += 1\n"
        "    return count\n",
        [["Hello World"], ["ALLCAPS"], ["nocaps"]],
        "",
    ),
    (
        "strings_017", "title_case",
        "Given a string s of lowercase words separated by spaces, return it with "
        "the first letter of every word capitalized. "
        "e.g. s='hello world' returns 'Hello World'.",
        "def title_case(s):\n"
        "    words = s.split()\n"
        "    result = []\n"
        "    for word in words:\n"
        "        result.append(word[0].upper() + word[1:])\n"
        "    return ' '.join(result)\n",
        [["hello world"], ["python is fun"], ["single"]],
        "Build the capitalized words in a list, then join() them back together with a space.",
    ),
    (
        "strings_018", "longest_word",
        "Given a string s of words separated by spaces, return the longest one. "
        "e.g. s='the quick brown fox' returns 'quick'.",
        "def longest_word(s):\n"
        "    words = s.split()\n"
        "    return max(words, key=len)\n",
        [["the quick brown fox"], ["a bb ccc"], ["equal ab cd"]],
        "",
    ),
    (
        "strings_019", "remove_character",
        "Given a string s and a character ch, return s with every occurrence of "
        "ch removed - built up one character at a time, not with replace(). "
        "e.g. s='banana', ch='a' returns 'bnn'.",
        "def remove_character(s, ch):\n"
        "    result = ''\n"
        "    for c in s:\n"
        "        if c != ch:\n            result += c\n"
        "    return result\n",
        [["banana", "a"], ["hello", "l"], ["xyz", "q"]],
        "",
    ),
    (
        "strings_020", "is_anagram",
        "Given two strings a and b, return whether they're anagrams of each "
        "other - the same letters, just rearranged. "
        "e.g. a='listen', b='silent' returns True.",
        "def is_anagram(a, b):\n    return sorted(a) == sorted(b)\n",
        [["listen", "silent"], ["hello", "world"], ["cat", "act"]],
        "",
    ),
]

# Each debug problem: (id, function_name, prompt, correct_solution, buggy_starter_code, list_of_args)
DEBUG_PROBLEMS = [
    (
        "strings_debug_001", "reverse_string",
        "Given a string s, this function is supposed to return it reversed — "
        "but it has a bug. Find it and fix it.",
        "def reverse_string(s):\n    return s[::-1]\n",
        "def reverse_string(s):\n    return s[::]\n",
        [["hello"], ["world"], ["ab"]],
    ),
    (
        "strings_debug_002", "count_character",
        "Given a string s and a character ch, this function is supposed to "
        "return how many times ch appears in s — but it has a bug. "
        "Find it and fix it.",
        "def count_character(s, ch):\n    return s.count(ch)\n",
        "def count_character(s, ch):\n"
        "    count = 0\n"
        "    for c in s:\n"
        "        if c == ch:\n            count = 1\n"
        "    return count\n",
        [["banana", "a"], ["hello", "l"], ["xyz", "a"]],
    ),
    (
        "strings_debug_003", "capitalize_first_letter",
        "Given a non-empty string s, this function is supposed to return it "
        "with its first letter capitalized — but it has a bug. "
        "Find it and fix it.",
        "def capitalize_first_letter(s):\n    return s[0].upper() + s[1:]\n",
        "def capitalize_first_letter(s):\n    return s[0].upper()\n",
        [["hello"], ["world"], ["a"]],
    ),
    (
        "strings_debug_004", "is_anagram",
        "Given two strings a and b, this function is supposed to return "
        "whether they're anagrams of each other — but it has a bug. "
        "Find it and fix it.",
        "def is_anagram(a, b):\n    return sorted(a) == sorted(b)\n",
        "def is_anagram(a, b):\n    return a == b\n",
        [["listen", "silent"], ["hello", "world"], ["cat", "act"]],
    ),
]


def main():
    """Writes all 24 Strings problem files and reports what it did."""
    written = write_topic("strings", "06_strings", WRITE_PROBLEMS, DEBUG_PROBLEMS)
    print(f"\nWrote {written} problem files.")


if __name__ == "__main__":
    main()
