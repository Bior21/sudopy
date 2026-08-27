"""Builds a Huffman tree from a character frequency map and derives codes.

Uses a min-heap (priority queue) to repeatedly pop the two
lowest-frequency nodes and merge them, the textbook greedy Huffman
construction algorithm; heapq gives O(n log n) construction rather than
O(n^2) from re-sorting a list on every merge. build_codes() then walks
the resulting tree to derive a prefix-code table. CHAR_BITS is 21 because
Unicode code points go up to 0x10FFFF, which needs 21 bits (2^21 =
2,097,152 > 1,114,112); fixed-width storage keeps tree serialization
simple, and the header overhead is negligible relative to the overall
file being compressed.
"""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field
from typing import Optional

CHAR_BITS = 21


@dataclass(order=True)
class Node:
    freq: int
    order: int = field(compare=True)
    char: Optional[str] = field(default=None, compare=False)
    left: Optional["Node"] = field(default=None, compare=False)
    right: Optional["Node"] = field(default=None, compare=False)

    def is_leaf(self) -> bool:
        """Determines whether this node holds a character or is internal.

        Returns:
            True if this is a leaf node (holds a character), False if
            it's an internal merge node.
        """
        return self.char is not None


def build_tree(freq_map: dict[str, int]) -> Node:
    """Builds a Huffman tree from a character frequency map.

    Repeatedly pops the two lowest-frequency nodes from a min-heap and
    merges them - the standard greedy Huffman construction algorithm.
    Using heapq gives O(n log n) construction instead of O(n^2) from
    re-sorting a list on every merge. `order` is a monotonically
    increasing tie-breaker so heapq never needs to compare Node.left/right,
    which would recurse into subtrees that aren't guaranteed orderable
    against each other.

    Args:
        freq_map: A mapping from character to how many times it occurs.

    Returns:
        The root Node of the resulting Huffman tree.

    Raises:
        ValueError: If freq_map is empty.
    """
    if not freq_map:
        raise ValueError("Cannot build a Huffman tree from an empty frequency map")

    counter = itertools.count()
    heap: list[Node] = [
        Node(freq=freq, order=next(counter), char=char)
        for char, freq in freq_map.items()
    ]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(
            freq=left.freq + right.freq,
            order=next(counter),
            left=left,
            right=right,
        )
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(root: Node) -> dict[str, str]:
    """Walks a Huffman tree and derives its prefix-code table.

    Args:
        root: The root of a Huffman tree, as returned by build_tree().

    Returns:
        A mapping from character to its bitstring code. If the tree has
        only one unique symbol, that symbol is assigned the code "0" so
        encode/decode still have a valid, non-empty code to work with.
    """
    codes: dict[str, str] = {}

    def dfs(node: Node, prefix: str) -> None:
        """Walks one subtree, recording a leaf's code as the bits taken to reach it."""
        if node.is_leaf():
            codes[node.char] = prefix or "0"
            return
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes
