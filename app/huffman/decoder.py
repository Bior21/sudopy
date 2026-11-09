"""
File: decoder.py
Author: Bior Madol Khom Bior
----------------------------
Undoes encoder.py. It reads the header, rebuilds the tree, and then walks
the tree one bit at a time: 0 goes left, 1 goes right, and reaching a
leaf gives one character before starting again from the root. It stops
after the number of characters stored in the header, so the padding bits
at the end are never read.
"""

import struct

from .bitio import BitReader
from .encoder import HEADER_FORMAT
from .tree import CHAR_BITS, Node

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def read_tree(reader: BitReader) -> Node:
    """Rebuilds a tree written by encoder.write_tree, reading it in preorder."""
    if reader.read_bit() == "1":
        char = chr(int(reader.read_bits(CHAR_BITS), 2))
        return Node(char=char)
    left = read_tree(reader)
    right = read_tree(reader)
    return Node(left=left, right=right)


def decode(data: bytes) -> str:
    """Decompresses bytes made by encoder.encode and returns the text."""
    text_length, padding = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    if text_length == 0:
        return ""

    reader = BitReader(data[HEADER_SIZE:], padding)
    root = read_tree(reader)

    # If the text used only one character, the tree is a single leaf.
    if root.is_leaf():
        return root.char * text_length

    chars = []
    node = root
    while len(chars) < text_length:
        if reader.read_bit() == "0":
            node = node.left
        else:
            node = node.right
        if node.is_leaf():
            chars.append(node.char)
            node = root
    return "".join(chars)
