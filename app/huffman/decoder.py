"""Reverses encoder.encode() to reconstruct the original text.

Reads the header, reconstructs the tree from its serialized form, then
walks the tree one bit at a time (root -> leaf -> root -> leaf ...) to
reconstruct the original text via decode(). It stops after decoding
exactly `text_length` characters (from the header), which is what lets
it safely ignore the padding bits at the end of the stream without
needing an explicit end-of-stream marker.
"""

from __future__ import annotations

import struct

from .bitio import BitReader
from .tree import CHAR_BITS, Node

_HEADER_FORMAT = ">IB"
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


def _deserialize_tree(reader: BitReader) -> Node:
    """Reads one subtree back out of a bitstream.

    Mirrors _serialize_tree's grammar: a leaf bit followed by 21 bits of
    character code, or an internal-node bit followed by two subtrees.

    Args:
        reader: The BitReader to read bits from.

    Returns:
        The reconstructed subtree root.
    """
    bit = reader.read_bit()
    if bit == "1":
        char_bits = reader.read_bits(CHAR_BITS)
        char = chr(int(char_bits, 2))
        return Node(freq=0, order=0, char=char)
    left = _deserialize_tree(reader)
    right = _deserialize_tree(reader)
    return Node(freq=0, order=0, left=left, right=right)


def decode(data: bytes) -> str:
    """Reverses encode(): reconstructs the original text from compressed bytes.

    Args:
        data: The compressed bytes produced by encode().

    Returns:
        The original text.
    """
    text_length, padding = struct.unpack(_HEADER_FORMAT, data[:_HEADER_SIZE])
    if text_length == 0:
        return ""

    reader = BitReader(data[_HEADER_SIZE:], padding)
    root = _deserialize_tree(reader)

    # Edge case: only one unique symbol in the original text means the
    # tree is a single leaf with no children - there's nothing to walk.
    if root.is_leaf():
        return root.char * text_length

    chars: list[str] = []
    node = root
    while len(chars) < text_length:
        bit = reader.read_bit()
        node = node.left if bit == "0" else node.right
        if node.is_leaf():
            chars.append(node.char)
            node = root

    return "".join(chars)
