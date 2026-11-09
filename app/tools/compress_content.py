"""
File: compress_content.py
Author: Bior Madol Khom Bior
----------------------------
Rebuilds content.huff from the content folder. Run this before packaging
the app, from inside app/:

    python3 -m tools.compress_content
"""

from pathlib import Path

from huffman.archive import compress_content

APP_DIR = Path(__file__).parent.parent


def main():
    """Compresses app/content into app/content.huff."""
    archive_path = APP_DIR / "content.huff"
    compress_content(APP_DIR / "content", archive_path)
    print(f"Archive written to {archive_path}")


if __name__ == "__main__":
    main()
