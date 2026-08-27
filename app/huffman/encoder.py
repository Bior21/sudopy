"""Encodes a string into a compressed byte string using Huffman coding.

The output is self-contained: the tree is serialized into the header, so
decode() needs nothing but the bytes this produces. The binary format is
a 4-byte original text length, a 1-byte padding bit count (0-7), the
serialized tree, and the encoded data, with the tree and data packed
together into one bitstream and padded to a byte boundary at the very
end (see BitWriter.to_bytes). The tree serialization grammar is
self-terminating and needs no length prefix: a leaf node is '1' followed
by 21 bits of the character's Unicode code point, and an internal node
is '0' followed by its left and right subtrees.
"""

from __future__ import annotations

import struct

from .bitio import BitWriter
from .tree import CHAR_BITS, Node, build_codes, build_tree

_HEADER_FORMAT = ">IB"  # uint32 text length, uint8 padding
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


def _serialize_tree(node: Node, writer: BitWriter) -> None:
    """Writes a subtree into a bitstream using the leaf/internal-node grammar.

    Args:
        node: The subtree root to serialize.
        writer: The BitWriter to append bits to.
    """
    if node.is_leaf():
        writer.write_bit(1)
        writer.write_bits(format(ord(node.char), f"0{CHAR_BITS}b"))
    else:
        writer.write_bit(0)
        _serialize_tree(node.left, writer)
        _serialize_tree(node.right, writer)


def encode(text: str) -> bytes:
    """Compresses text into a self-contained Huffman-coded byte string.

    Args:
        text: The text to compress.

    Returns:
        The compressed bytes, including a header and serialized tree so
        decode() needs nothing else to reconstruct the original text.
    """
    if text == "":
        return struct.pack(_HEADER_FORMAT, 0, 0)

    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1

    root = build_tree(freq)
    codes = build_codes(root)

    writer = BitWriter()
    _serialize_tree(root, writer)
    for ch in text:
        writer.write_bits(codes[ch])

    data_bytes, padding = writer.to_bytes()
    header = struct.pack(_HEADER_FORMAT, len(text), padding)
    return header + data_bytes
