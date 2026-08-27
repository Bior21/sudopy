"""Packages the content/ directory into a single compressed archive.

A packaging-time script that Huffman-compresses every problem JSON file
under content/ into one content.huff archive, to be bundled inside the
app (see packaging/build.spec). The archive format is a 4-byte entry
count, then per entry a 2-byte relative path length, the relative path
bytes (utf-8), a 4-byte compressed block length, and the compressed
block bytes from huffman.encoder.encode(). At runtime, the packaged app
calls decompress_content() to unpack this archive into a temp directory
that ProblemLoader can then read normally, so ProblemLoader itself never
needs to know Huffman is involved. This is a deliberate, clearly-scoped
use of the from-scratch Huffman module: it compresses problem content
specifically, not the interpreter or GUI framework bundled by
PyInstaller, which is handled by zstd/zip at the OS packaging layer as a
separate concern.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

from huffman.encoder import encode
from huffman.decoder import decode

CONTENT_DIR = Path(__file__).parent / "content"
ARCHIVE_PATH = Path(__file__).parent / "content.huff"


def compress_content(content_dir: Path, archive_path: Path) -> None:
    """Huffman-compresses every JSON file under content_dir into one archive.

    Args:
        content_dir: The directory containing topic subfolders of problem
            JSON files.
        archive_path: Where to write the resulting archive.

    Raises:
        RuntimeError: If content_dir contains no JSON files.
    """
    json_files = sorted(content_dir.rglob("*.json"))
    if not json_files:
        raise RuntimeError(f"No .json files found under {content_dir}")

    entries = []
    total_original = 0
    total_compressed = 0

    for file_path in json_files:
        relative_path = file_path.relative_to(content_dir).as_posix()
        text = file_path.read_text(encoding="utf-8")
        compressed = encode(text)

        entries.append((relative_path, compressed))
        total_original += len(text.encode("utf-8"))
        total_compressed += len(compressed)

    with open(archive_path, "wb") as f:
        f.write(struct.pack(">I", len(entries)))
        for relative_path, compressed in entries:
            path_bytes = relative_path.encode("utf-8")
            f.write(struct.pack(">H", len(path_bytes)))
            f.write(path_bytes)
            f.write(struct.pack(">I", len(compressed)))
            f.write(compressed)

    ratio = (1 - total_compressed / total_original) * 100 if total_original else 0
    print(f"Compressed {len(entries)} files: {total_original} -> {total_compressed} bytes "
          f"({ratio:.1f}% reduction)")
    print(f"Archive written to {archive_path}")


def decompress_content(archive_path: Path, output_dir: Path) -> None:
    """Unpacks a content.huff archive back into plain JSON files.

    Used by the runtime loader path in main.py and by round-trip
    tests/verification.

    Args:
        archive_path: The compressed archive to read.
        output_dir: The directory to write the decompressed JSON files into.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(archive_path, "rb") as f:
        (num_entries,) = struct.unpack(">I", f.read(4))
        for _ in range(num_entries):
            (path_len,) = struct.unpack(">H", f.read(2))
            relative_path = f.read(path_len).decode("utf-8")
            (data_len,) = struct.unpack(">I", f.read(4))
            compressed = f.read(data_len)

            text = decode(compressed)
            out_path = output_dir / relative_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")


def main():
    """Regenerates content.huff from the current content/ directory."""
    compress_content(CONTENT_DIR, ARCHIVE_PATH)


if __name__ == "__main__":
    main()
