import zlib

import pytest

from huffman.encoder import encode
from huffman.decoder import decode
from huffman.tree import build_tree, build_codes


def roundtrip(text: str) -> str:
    return decode(encode(text))


def test_empty_string():
    assert roundtrip("") == ""


def test_single_character():
    assert roundtrip("a") == "a"


def test_single_repeated_character():
    assert roundtrip("aaaaaaaaaa") == "aaaaaaaaaa"


def test_two_distinct_characters():
    assert roundtrip("abababab") == "abababab"


def test_typical_sentence():
    text = "the quick brown fox jumps over the lazy dog"
    assert roundtrip(text) == text


def test_whitespace_and_punctuation():
    text = "Hello, world!\nThis has\ttabs and\nnewlines."
    assert roundtrip(text) == text


def test_json_like_content():
    text = '{"id": "loops_001", "prompt": "Read an integer N", "expected_output": "15"}'
    assert roundtrip(text) == text


def test_unicode_characters():
    text = "café résumé naïve 日本語 emoji: 🎉"
    assert roundtrip(text) == text


def test_larger_repetitive_text_compresses_smaller_than_original():
    # Repetitive text has skewed frequency distribution, which is exactly
    # what Huffman coding exploits.
    text = "abcabcabcabc" * 200
    compressed = encode(text)
    original_size = len(text.encode("utf-8"))
    assert len(compressed) < original_size


def test_build_codes_gives_shorter_codes_to_more_frequent_chars():
    freq = {"a": 100, "b": 10, "c": 1}
    root = build_tree(freq)
    codes = build_codes(root)
    assert len(codes["a"]) <= len(codes["b"]) <= len(codes["c"])


def test_build_codes_are_prefix_free():
    # No code should be a prefix of another - this is what makes the
    # encoding unambiguous to decode without a separator between symbols.
    freq = {"a": 5, "b": 3, "c": 2, "d": 1, "e": 1}
    root = build_tree(freq)
    codes = build_codes(root)
    code_list = list(codes.values())
    for i, code_a in enumerate(code_list):
        for code_b in code_list[i + 1:]:
            assert not code_b.startswith(code_a)
            assert not code_a.startswith(code_b)


def test_build_tree_rejects_empty_freq_map():
    with pytest.raises(ValueError):
        build_tree({})


def test_compression_ratio_vs_zlib_on_sample_problem_text():
    """
    Not an assertion of superiority - Huffman alone (no LZ77-style
    substring matching) is expected to compress worse than zlib/DEFLATE
    on real text. This test documents that honestly rather than pretending
    otherwise, and just sanity-checks both produce valid, smaller output.
    """
    sample = (
        "Read an integer N, then print the sum of all integers from 1 to N. "
        "Read an integer N, then print the sum of all integers from 1 to N. "
        "Use a for loop with range(1, n + 1) to accumulate the total."
    )
    original_size = len(sample.encode("utf-8"))
    huffman_size = len(encode(sample))
    zlib_size = len(zlib.compress(sample.encode("utf-8")))

    assert huffman_size < original_size
    assert zlib_size < original_size
    # Document (not assert as a hard requirement) that zlib tends to win
    # on real text due to LZ77 substring matching - printed for visibility
    # when running with -s, doesn't fail the test either way.
    print(f"\noriginal={original_size} huffman={huffman_size} zlib={zlib_size}")
