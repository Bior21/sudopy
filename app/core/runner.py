"""Executes student-submitted code in an isolated subprocess.

Runs a string of Python source with a given stdin and returns what
happened, via run_code() and the ExecutionResult it produces. Subprocess
isolation, rather than in-process exec(), means a crash or infinite loop
in student code can't take down the GUI process, a hard wall-clock
timeout can be enforced and the process killed, and stdout/stderr capture
is clean without redirection hacks. This module knows nothing about
grading or problems - that's core/grader.py's job.

In a normal Python environment, sys.executable is a real interpreter
that understands "-c <code>". In a PyInstaller-frozen build, sys.executable
is the packaged app itself, which does not - so a frozen build instead
writes source_code to a temp file and re-invokes itself with
FROZEN_EXEC_FLAG, which main.py recognizes and handles by running that
file as a standalone script instead of launching the GUI.

On timeout, the whole process tree is killed, not just the immediate
child. A plain Popen.kill() only signals the process we directly
launched; a frozen build's bootloader forks an inner process to run the
unpacked interpreter, and killing only the outer one can orphan that
inner process, leaving it running the student's infinite loop forever.
Launching in a new session/process group and killing the whole group
closes that gap.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TIMEOUT_SECONDS = 5

FROZEN_EXEC_FLAG = "--sudopy-run-code"


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    timed_out: bool
    returncode: int | None

    @property
    def crashed(self) -> bool:
        """Whether the process ran to completion but exited with an error.

        Returns:
            True if the process returned a nonzero exit code (and did not
            time out), False otherwise.
        """
        return self.returncode is not None and self.returncode != 0

    @property
    def succeeded(self) -> bool:
        """Whether the process ran to completion without crashing or hanging.

        Returns:
            True if the process neither timed out nor crashed.
        """
        return not self.timed_out and not self.crashed


def _build_command(source_code: str) -> tuple[list[str], Path | None]:
    """Builds the subprocess argv used to run source_code.

    In a normal Python install, sys.executable understands "-c <code>"
    directly. In a frozen build, source_code is written to a temp file
    instead, and the packaged app is re-invoked with FROZEN_EXEC_FLAG and
    that file's path - see this module's docstring for why.

    Args:
        source_code: The Python source to execute.

    Returns:
        A tuple of (argv, temp_file). temp_file is the Path to a
        temporary file the caller must delete once the subprocess exits,
        or None if no temp file was created.
    """
    if not getattr(sys, "frozen", False):
        return [sys.executable, "-c", source_code], None

    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(source_code)
    temp_file = Path(path)
    return [sys.executable, FROZEN_EXEC_FLAG, str(temp_file)], temp_file


def _start_new_process_group_kwargs() -> dict:
    """Builds the Popen kwargs that launch a child into its own process group.

    This is what makes it possible to kill the child's entire process
    tree later, rather than just the child itself.

    Returns:
        A dict of keyword arguments to pass to subprocess.Popen.
    """
    if sys.platform == "win32":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _kill_process_tree(process: subprocess.Popen) -> None:
    """Kills a subprocess and every process it spawned.

    Args:
        process: The subprocess to kill, launched via
            _start_new_process_group_kwargs() so it heads its own
            process group.
    """
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            capture_output=True,
        )
        return

    try:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except ProcessLookupError:
        pass  # already exited on its own


def run_code(
    source_code: str,
    stdin_input: str = "",
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> ExecutionResult:
    """Runs source_code as a standalone Python script in an isolated subprocess.

    Args:
        source_code: The Python source to execute.
        stdin_input: Text fed to the process's stdin, for input() calls.
        timeout: Wall-clock seconds to allow before the process is killed.

    Returns:
        An ExecutionResult with the captured stdout, stderr, and status.
    """
    command, temp_file = _build_command(source_code)
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        **_start_new_process_group_kwargs(),
    )
    try:
        stdout, stderr = process.communicate(input=stdin_input, timeout=timeout)
        return ExecutionResult(
            stdout=stdout,
            stderr=stderr,
            timed_out=False,
            returncode=process.returncode,
        )
    except subprocess.TimeoutExpired:
        _kill_process_tree(process)
        stdout, stderr = process.communicate()  # reap the process, drain any output
        return ExecutionResult(
            stdout=stdout or "",
            stderr=stderr or "",
            timed_out=True,
            returncode=None,
        )
    finally:
        if temp_file is not None:
            temp_file.unlink(missing_ok=True)
