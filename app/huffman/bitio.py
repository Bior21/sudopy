"""Minimal bit-level I/O helpers, via the BitWriter and BitReader classes.

Deliberately built by hand rather than using a third-party bitarray
library, since demonstrating real bit packing - not just concatenating
'0'/'1' strings and pretending that's compression - is the point of this
module. Internally it still builds up a string of '0'/'1' characters
before packing into bytes; this is clear and easy to verify correct,
which matters more here than raw performance, since this module only
ever processes problem-text-sized content (KBs), not gigabytes.
"""

from __future__ import annotations


class BitWriter:
    """Accumulates individual bits and packs them into bytes."""

    def __init__(self):
        """Creates an empty BitWriter with no bits written yet."""
        self._chunks: list[str] = []

    def write_bit(self, bit: int) -> None:
        """Appends a single bit.

        Args:
            bit: 0 or 1 (any truthy/falsy int is treated as 1/0).
        """
        self._chunks.append("1" if bit else "0")

    def write_bits(self, bitstring: str) -> None:
        """Appends a run of bits.

        Args:
            bitstring: A string of '0'/'1' characters.
        """
        self._chunks.append(bitstring)

    def to_bytes(self) -> tuple[bytes, int]:
        """Packs all written bits into bytes, padding to a byte boundary.

        Returns:
            A tuple of (packed_bytes, padding_bit_count), where
            padding_bit_count is how many zero bits were appended at the
            end to reach a whole number of bytes.
        """
        bitstring = "".join(self._chunks)
        padding = (8 - len(bitstring) % 8) % 8
        bitstring += "0" * padding

        out = bytearray()
        for i in range(0, len(bitstring), 8):
            out.append(int(bitstring[i : i + 8], 2))
        return bytes(out), padding


class BitReader:
    """Reads individual bits back out of a byte string, in order."""

    def __init__(self, data: bytes, padding: int = 0):
        """Unpacks data into a bitstring, dropping the trailing padding bits.

        Args:
            data: The compressed bytes to read bits from.
            padding: How many trailing bits are padding and should be dropped.
        """
        bits = "".join(f"{byte:08b}" for byte in data)
        if padding:
            bits = bits[:-padding]
        self._bits = bits
        self._pos = 0

    def read_bit(self) -> str:
        """Reads and consumes the next single bit.

        Returns:
            The next bit, as the character '0' or '1'.
        """
        bit = self._bits[self._pos]
        self._pos += 1
        return bit

    def read_bits(self, n: int) -> str:
        """Reads and consumes the next n bits.

        Args:
            n: How many bits to read.

        Returns:
            The next n bits, as a string of '0'/'1' characters.
        """
        chunk = self._bits[self._pos : self._pos + n]
        self._pos += n
        return chunk

    def has_more(self) -> bool:
        """Determines whether there are unread bits remaining.

        Returns:
            True if more bits remain to be read, False otherwise.
        """
        return self._pos < len(self._bits)
