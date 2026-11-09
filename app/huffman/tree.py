"""
File: tree.py
Author: Bior Madol Khom Bior
----------------------------
Builds a Huffman tree and the code for each character. Frequent
characters get short codes and rare ones get long codes, which is what
makes the encoded text smaller.

The tree is built with a min-heap (priority queue): repeatedly take the
two least frequent nodes and join them under a new parent. With n
different characters this takes O(n log n) time.
"""

import heapq

# Each character is stored in the tree header as its Unicode number. The
# largest Unicode number is 0x10FFFF, which needs 21 bits.
CHAR_BITS = 21


class Node:
    """A tree node. Leaves hold a character; inner nodes have two children."""

    def __init__(self, char=None, left=None, right=None):
        """Makes a leaf (give char) or an inner node (give left and right)."""
        self.char = char
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """True if this node holds a character."""
        return self.char is not None


def build_tree(frequencies: dict[str, int]) -> Node:
    """
    Builds the Huffman tree from a map of character -> number of times it
    appears, and returns the root.

    Each heap entry is (frequency, order, node). The order number breaks
    ties between equal frequencies, so the heap never has to compare two
    Nodes directly.
    """
    if not frequencies:
        raise ValueError("Cannot build a Huffman tree from an empty frequency map")

    heap = []
    order = 0
    for char, frequency in frequencies.items():
        heap.append((frequency, order, Node(char=char)))
        order += 1
    heapq.heapify(heap)

    while len(heap) > 1:
        left_frequency, _, left = heapq.heappop(heap)
        right_frequency, _, right = heapq.heappop(heap)
        parent = Node(left=left, right=right)
        heapq.heappush(heap, (left_frequency + right_frequency, order, parent))
        order += 1

    return heap[0][2]


def build_codes(root: Node) -> dict[str, str]:
    """
    Returns a map of character -> code, where a code is a string of "0"s
    and "1"s: "0" for each step left and "1" for each step right on the way
    from the root to that character's leaf.
    """
    codes = {}
    add_codes(root, "", codes)
    return codes


def add_codes(node: Node, path: str, codes: dict[str, str]) -> None:
    """
    Recursively records the code of every leaf below node. path is the
    route taken so far. If the whole tree is one leaf (the text used only
    one character), that character gets the code "0".
    """
    if node.is_leaf():
        if path == "":
            path = "0"
        codes[node.char] = path
        return
    add_codes(node.left, path + "0", codes)
    add_codes(node.right, path + "1", codes)
