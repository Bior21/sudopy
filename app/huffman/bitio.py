"""
File: bitio.py
Author: Bior Madol Khom Bior
----------------------------
Writes and reads single bits. Files can only store whole bytes, so
BitWriter collects bits and packs every 8 of them into one byte, adding
zero bits at the end to fill the last byte. BitReader unpacks the bytes
again and hands the bits back one at a time.

Bits are kept as a string of "0" and "1" characters. That is not the
fastest way, but it is easy to check, and the problem files are small.
"""


class BitWriter:
    """Collects bits and packs them into bytes."""

    def __init__(self):
        """Starts with no bits written."""
        self._bits = []

    def write_bit(self, bit: int) -> None:
        """Adds one bit (0 or 1)."""
        if bit:
            self._bits.append("1")
        else:
            self._bits.append("0")

    def write_bits(self, bits: str) -> None:
        """Adds several bits, given as a string such as "0110"."""
        self._bits.append(bits)

    def to_bytes(self) -> tuple[bytes, int]:
        """
        Packs the bits into bytes. Returns the bytes and how many zero bits
        were added at the end to fill the last byte (between 0 and 7).
        """
        bits = "".join(self._bits)
        padding = (8 - len(bits) % 8) % 8
        bits += "0" * padding

        packed = bytearray()
        for start in range(0, len(bits), 8):
            packed.append(int(bits[start:start + 8], 2))
        return bytes(packed), padding


class BitReader:
    """Reads bits back out of bytes, in the order they were written."""

    def __init__(self, data: bytes, padding: int = 0):
        """Unpacks the bytes into bits, dropping the padding bits at the end."""
        byte_texts = []
        for byte in data:
            byte_texts.append(format(byte, "08b"))   # e.g. 5 -> "00000101"
        bits = "".join(byte_texts)
        if padding > 0:
            bits = bits[:-padding]
        self._bits = bits
        self._position = 0

    def read_bit(self) -> str:
        """Returns the next bit as "0" or "1"."""
        bit = self._bits[self._position]
        self._position += 1
        return bit

    def read_bits(self, count: int) -> str:
        """Returns the next count bits as a string."""
        bits = self._bits[self._position:self._position + count]
        self._position += count
        return bits
