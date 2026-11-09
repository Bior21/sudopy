"""
File: encoder.py
Author: Bior Madol Khom Bior
----------------------------
Compresses text with Huffman coding. The result holds everything needed
to decompress it, in this order:

    4 bytes   how many characters the text has
    1 byte    how many padding bits were added at the end
    the tree, written as bits (see write_tree)
    the text, with each character replaced by its code
"""

import struct

from .bitio import BitWriter
from .tree import CHAR_BITS, Node, build_codes, build_tree

# ">IB" means: big-endian, one 4-byte unsigned int, one 1-byte unsigned int.
HEADER_FORMAT = ">IB"


def write_tree(node: Node, writer: BitWriter) -> None:
    """
    Writes the tree in preorder. A leaf is written as a 1 followed by its
    character's 21-bit Unicode number. An inner node is written as a 0
    followed by its left subtree and then its right subtree.
    """
    if node.is_leaf():
        writer.write_bit(1)
        writer.write_bits(format(ord(node.char), f"0{CHAR_BITS}b"))
    else:
        writer.write_bit(0)
        write_tree(node.left, writer)
        write_tree(node.right, writer)


def count_characters(text: str) -> dict[str, int]:
    """Returns how many times each character appears in the text."""
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


def encode(text: str) -> bytes:
    """Compresses the text and returns the compressed bytes."""
    if text == "":
        return struct.pack(HEADER_FORMAT, 0, 0)

    root = build_tree(count_characters(text))
    codes = build_codes(root)

    writer = BitWriter()
    write_tree(root, writer)
    for char in text:
        writer.write_bits(codes[char])

    data, padding = writer.to_bytes()
    header = struct.pack(HEADER_FORMAT, len(text), padding)
    return header + data
