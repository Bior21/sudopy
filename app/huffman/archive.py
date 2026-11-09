"""
File: archive.py
Author: Bior Madol Khom Bior
----------------------------
Packs every problem file into one compressed file, content.huff, which
ships inside the app. When the packaged app starts, it unpacks the
archive into a temporary folder and loads the problems from there.

The archive is laid out like this:

    4 bytes   how many files it holds
    then, for each file:
      2 bytes   length of the file's path
      the path, such as "05_loops/loops_001.json"
      4 bytes   length of the compressed file
      the file, compressed by encoder.encode
"""

import struct
from pathlib import Path

from .decoder import decode
from .encoder import encode


def compress_content(content_dir: Path, archive_path: Path) -> None:
    """Compresses every .json file under content_dir into one archive file."""
    json_files = sorted(content_dir.rglob("*.json"))
    if not json_files:
        raise RuntimeError(f"No .json files found under {content_dir}")

    original_size = 0
    compressed_size = 0
    with open(archive_path, "wb") as archive:
        archive.write(struct.pack(">I", len(json_files)))
        for file_path in json_files:
            text = file_path.read_text(encoding="utf-8")
            compressed = encode(text)
            path_bytes = file_path.relative_to(content_dir).as_posix().encode("utf-8")

            archive.write(struct.pack(">H", len(path_bytes)))
            archive.write(path_bytes)
            archive.write(struct.pack(">I", len(compressed)))
            archive.write(compressed)

            original_size += len(text.encode("utf-8"))
            compressed_size += len(compressed)

    saved = (1 - compressed_size / original_size) * 100
    print(f"Compressed {len(json_files)} files: {original_size} -> {compressed_size} bytes "
          f"({saved:.1f}% smaller)")


def decompress_content(archive_path: Path, output_dir: Path) -> None:
    """Unpacks an archive made by compress_content back into JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(archive_path, "rb") as archive:
        file_count = struct.unpack(">I", archive.read(4))[0]
        for _ in range(file_count):
            path_length = struct.unpack(">H", archive.read(2))[0]
            relative_path = archive.read(path_length).decode("utf-8")
            data_length = struct.unpack(">I", archive.read(4))[0]
            text = decode(archive.read(data_length))

            out_path = output_dir / relative_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
