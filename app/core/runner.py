"""
File: runner.py
Author: Bior Madol Khom Bior
----------------------------
Runs a student's Python code in a separate process and records what it
printed. Using a separate process instead of exec() means a crash or an
infinite loop in the student's code can never freeze or crash the app:
if the code runs too long, we simply kill its process.

In the packaged app there is no "python" program to start, only Sudopy
itself. So the packaged app saves the code to a temporary file and
starts a second copy of itself with RUN_CODE_FLAG, which tells main.py
to run that file instead of opening a window.
"""

import os
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass

TIMEOUT_SECONDS = 5
RUN_CODE_FLAG = "--sudopy-run-code"


@dataclass
class ExecutionResult:
    stdout: str              # everything the code printed
    stderr: str              # the error message, if it crashed
    timed_out: bool
    returncode: int | None   # None when the process was killed

    @property
    def crashed(self) -> bool:
        """True if the code finished but stopped with an error."""
        return self.returncode is not None and self.returncode != 0

    @property
    def succeeded(self) -> bool:
        """True if the code finished without crashing or timing out."""
        return not self.timed_out and not self.crashed


def is_packaged_app() -> bool:
    """True when running as the packaged app (PyInstaller sets sys.frozen)."""
    return getattr(sys, "frozen", False)


def save_to_temp_file(source_code: str) -> str:
    """Saves the code to a new temporary .py file and returns its path."""
    file_descriptor, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
        file.write(source_code)
    return path


def start_process(command: list) -> subprocess.Popen:
    """
    Starts the command as a new process in its own process group, so that
    later we can kill it together with any processes it started.
    """
    if sys.platform == "win32":
        return subprocess.Popen(
            command,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    return subprocess.Popen(
        command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )


def kill_process_group(process: subprocess.Popen) -> None:
    """
    Kills the process and every process it started. The packaged app starts
    an inner process of its own, so killing only the outer one could leave
    the student's infinite loop running in the background.
    """
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True)
        return
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except ProcessLookupError:
        pass  # it already finished on its own


def run_code(source_code: str, stdin_input: str = "", timeout: int = TIMEOUT_SECONDS) -> ExecutionResult:
    """
    Runs the code as its own Python program, typing stdin_input into it for
    any input() calls. Kills it if it runs longer than timeout seconds.
    """
    temp_file = None
    if is_packaged_app():
        temp_file = save_to_temp_file(source_code)
        command = [sys.executable, RUN_CODE_FLAG, temp_file]
    else:
        command = [sys.executable, "-c", source_code]

    process = start_process(command)
    try:
        stdout, stderr = process.communicate(input=stdin_input, timeout=timeout)
        return ExecutionResult(stdout, stderr, timed_out=False, returncode=process.returncode)
    except subprocess.TimeoutExpired:
        kill_process_group(process)
        stdout, stderr = process.communicate()  # wait for it to exit and collect any output
        return ExecutionResult(stdout or "", stderr or "", timed_out=True, returncode=None)
    finally:
        if temp_file is not None:
            os.remove(temp_file)
