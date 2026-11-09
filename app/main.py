"""
File: main.py
Author: Bior Madol Khom Bior
----------------------------
Starts Sudopy. While developing, the problems are read straight from the
content folder. In the packaged app, the compressed content.huff is
unpacked into a temporary folder first, and the problems are read from
there.

The packaged app is also started a second time by runner.py, with
RUN_CODE_FLAG, to run a student's code. In that case this file runs the
code instead of opening a window.
"""

import runpy
import sys
import tempfile
from pathlib import Path

from core.runner import RUN_CODE_FLAG, is_packaged_app


def find_content_dir() -> Path:
    """Returns the folder to load problems from (see the file header)."""
    if not is_packaged_app():
        return Path(__file__).parent / "content"

    from huffman.archive import decompress_content

    # PyInstaller unpacks the app's bundled files into the folder sys._MEIPASS.
    archive_path = Path(sys._MEIPASS) / "content.huff"
    content_dir = Path(tempfile.mkdtemp(prefix="sudopy_content_"))
    decompress_content(archive_path, content_dir)
    return content_dir


def main():
    """Runs a student's code file if asked to, otherwise opens the app window."""
    if len(sys.argv) >= 3 and sys.argv[1] == RUN_CODE_FLAG:
        runpy.run_path(sys.argv[2], run_name="__main__")
        return

    from gui.main_window import MainWindow

    window = MainWindow(find_content_dir())
    window.mainloop()


if __name__ == "__main__":
    main()
