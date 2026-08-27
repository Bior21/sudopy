"""Executes student-submitted code in an isolated subprocess.

Runs a string of Python source with a given stdin and returns what
happened, via run_code() and the ExecutionResult it produces. Subprocess
isolation, rather than in-process exec(), means a crash or infinite loop
in student code can't take down the GUI process, a hard wall-clock
timeout can be enforced and the process killed, and stdout/stderr capture
is clean without redirection hacks. This module knows nothing about
grading or problems - that's core/grader.py's job.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass


DEFAULT_TIMEOUT_SECONDS = 5


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


def run_code(
    source_code: str,
    stdin_input: str = "",
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> ExecutionResult:
    """Runs source_code as a standalone Python script in an isolated subprocess.

    Uses sys.executable so it works whether running from a normal Python
    install or a PyInstaller-bundled interpreter.

    Args:
        source_code: The Python source to execute.
        stdin_input: Text fed to the process's stdin, for input() calls.
        timeout: Wall-clock seconds to allow before the process is killed.

    Returns:
        An ExecutionResult with the captured stdout, stderr, and status.
    """
    try:
        completed = subprocess.run(
            [sys.executable, "-c", source_code],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return ExecutionResult(
            stdout=completed.stdout,
            stderr=completed.stderr,
            timed_out=False,
            returncode=completed.returncode,
        )
    except subprocess.TimeoutExpired as e:
        return ExecutionResult(
            stdout=e.stdout or "",
            stderr=e.stderr or "",
            timed_out=True,
            returncode=None,
        )
