"""Application entry point for the Sudopy desktop app.

Launches the Tkinter GUI pointed at a content directory. In a packaged
(PyInstaller-frozen) build, content.huff is bundled as a data file
alongside the executable; on startup it's decompressed into a temp
directory and the GUI is pointed there, which is what makes the Huffman
module load-bearing in the shipped product rather than a demo script. In
development (plain `python3 main.py`), the GUI points directly at the
plain content/ folder, so iterating on problem content doesn't require
re-running compress_content.py every time.

A frozen build is also re-invoked as a subprocess to run student code
(see core/runner.py's FROZEN_EXEC_FLAG). When launched that way, this
module runs the given file as a standalone script instead of starting
the GUI, since a frozen sys.executable can't be called with "-c <code>"
the way a real Python interpreter can.
"""

import runpy
import sys
import tempfile
from pathlib import Path

from core.runner import FROZEN_EXEC_FLAG


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


def _run_as_script(script_path: str) -> None:
    """Executes a file as a standalone script, the way `python file.py` would.

    Used only when a frozen build re-invokes itself with FROZEN_EXEC_FLAG
    to run student code - see this module's docstring and
    core/runner.py for why.

    Args:
        script_path: Path to the Python file to execute.
    """
    runpy.run_path(script_path, run_name="__main__")


def main():
    """Launches the Sudopy desktop application, or runs student code.

    If invoked with FROZEN_EXEC_FLAG - which only happens when a frozen
    build re-invokes itself from core/runner.py - runs the given file
    instead of starting the GUI. Otherwise resolves the content
    directory, builds the main window, and starts the Tkinter event loop.
    """
    if len(sys.argv) >= 3 and sys.argv[1] == FROZEN_EXEC_FLAG:
        _run_as_script(sys.argv[2])
        return

    from gui.main_window import MainWindow

    content_dir = resolve_content_dir()
    app = MainWindow(content_dir)
    app.mainloop()


if __name__ == "__main__":
    main()
