"""Application entry point for the Sudopy desktop app.

Launches the Tkinter GUI pointed at a content directory. In a packaged
(PyInstaller-frozen) build, content.huff is bundled as a data file
alongside the executable; on startup it's decompressed into a temp
directory and the GUI is pointed there, which is what makes the Huffman
module load-bearing in the shipped product rather than a demo script. In
development (plain `python3 main.py`), the GUI points directly at the
plain content/ folder, so iterating on problem content doesn't require
re-running compress_content.py every time.
"""

import sys
import tempfile
from pathlib import Path

from gui.main_window import MainWindow


def _is_frozen() -> bool:
    """Determines whether the app is running as a packaged executable.

    Checks the `frozen` attribute that PyInstaller's bootloader sets on
    the `sys` module at runtime; it is only present in a packaged build.

    Returns:
        True if running inside a PyInstaller-built executable, False if
        running as a normal Python script.
    """
    return getattr(sys, "frozen", False)


def _bundled_resource_dir() -> Path:
    """Finds the directory where PyInstaller extracts bundled data files.

    Reads `sys._MEIPASS`, which PyInstaller's bootloader sets to a
    temporary extraction directory at runtime. It only exists when the
    app is frozen.

    Returns:
        The path to the bundled resource directory.
    """
    return Path(getattr(sys, "_MEIPASS", "."))


def resolve_content_dir() -> Path:
    """Determines which directory the GUI should load problems from.

    In a packaged build, the bundled content.huff archive is decompressed
    into a fresh temporary directory. In development, the plain content/
    folder is used directly so problem edits don't require recompressing.

    Returns:
        The path to a directory containing plain problem JSON files.
    """
    if _is_frozen():
        from compress_content import decompress_content

        archive_path = _bundled_resource_dir() / "content.huff"
        temp_dir = Path(tempfile.mkdtemp(prefix="sudopy_content_"))
        decompress_content(archive_path, temp_dir)
        return temp_dir

    return Path(__file__).parent / "content"


def main():
    """Launches the Sudopy desktop application.

    Resolves the content directory, builds the main window, and starts
    the Tkinter event loop.
    """
    content_dir = resolve_content_dir()
    app = MainWindow(content_dir)
    app.mainloop()


if __name__ == "__main__":
    main()
