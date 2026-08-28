"""Displays the outcome of running and grading a student's code.

Hidden until the student runs their code for the first time on the
current problem - clear() unpacks the whole panel rather than just
emptying it. Once there's something to show, update_results() packs it
back and fills in an overall "X/Y tests passed" summary plus a compact
bordered table: one row per test case, with the input used (or the
function call, for a test that takes no input), the expected output,
what the student's code actually produced, and a pass/fail mark.
ResultsView is deliberately dumb and stateless - it just renders
whatever it's given via update_results(), with no knowledge of
runner/grader internals beyond the GradeResult shape.
"""

import tkinter as tk
from tkinter import ttk

_PASS_COLOR = "#1a7f37"
_FAIL_COLOR = "#cf222e"
_PASS_MARK = "✓"
_FAIL_MARK = "✗"
_BORDER_COLOR = "#D0D0D0"
_HEADER_BG = "#EFEFEF"
_CELL_BG = "white"
_TEXT_COLOR = "#1A1A1A"

_HEADERS = ("Input / Call", "Expected", "Got", "OK")
_HEADER_FONT = ("TkDefaultFont", 9, "bold")
_CELL_FONT = ("TkDefaultFont", 9)


class ResultsView(ttk.Frame):
    def __init__(self, parent):
        """Builds the summary label and table, without showing them yet.

        Args:
            parent: The Tkinter widget this frame is placed inside.
        """
        super().__init__(parent)
        self._pack_options = {"fill": "x"}

        self.status_label = ttk.Label(self, text="", font=("TkDefaultFont", 11, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 6))

        # A frame with a border-colored background, showing through the
        # 1px gaps left around each cell label, is the standard Tkinter
        # way to fake grid lines between cells.
        self.table_frame = tk.Frame(self, background=_BORDER_COLOR)
        self.table_frame.pack(fill="x")
        for col in range(3):
            self.table_frame.grid_columnconfigure(col, weight=1)

        self._build_header_row()

    def _build_header_row(self):
        """Builds the table's fixed header row of column titles."""
        for col, title in enumerate(_HEADERS):
            label = tk.Label(
                self.table_frame, text=title, font=_HEADER_FONT, foreground=_TEXT_COLOR,
                background=_HEADER_BG, padx=6, pady=2, anchor="w",
            )
            label.grid(row=0, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))

    def clear(self):
        """Hides the whole results panel until the next run."""
        self.pack_forget()

    def update_results(self, function_name, tests, grade_results):
        """Fills the table with one row per test case, plus an overall summary.

        Shows the panel, which is hidden by default until this is called.

        Args:
            function_name: The problem's function name, shown in the
                "Input / Call" column for a test that takes no input.
            tests: The problem's core.problem_loader.TestCase list that
                was run, in the same order as grade_results.
            grade_results: The core.grader.GradeResult produced for each
                test in tests.
        """
        self._update_summary(grade_results)
        self._clear_rows()
        for row, (test, grade_result) in enumerate(zip(tests, grade_results), start=1):
            self._add_row(row, function_name, test, grade_result)
        self.pack(**self._pack_options)

    def _update_summary(self, grade_results):
        """Sets the overall "X/Y tests passed" status label.

        Args:
            grade_results: The GradeResult produced for each test run.
        """
        passed_count = sum(1 for g in grade_results if g.passed)
        total = len(grade_results)
        if passed_count == total:
            self.status_label.config(text=f"All {total} test(s) passed!", foreground=_PASS_COLOR)
        else:
            self.status_label.config(
                text=f"{passed_count}/{total} test(s) passed", foreground=_FAIL_COLOR
            )

    def _clear_rows(self):
        """Removes every data row from the table, keeping the header row."""
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) != 0:
                widget.destroy()

    def _add_row(self, row, function_name, test, grade_result):
        """Adds one test's row to the results table.

        Args:
            row: The row's grid position (row 0 is the header, so this
                is 1-based).
            function_name: The problem's function name, used as the
                "Input / Call" cell when the test has no input.
            test: The core.problem_loader.TestCase that was run.
            grade_result: The GradeResult produced by grading it.
        """
        input_display = _flatten(test.input) if test.input.strip() else f"{function_name}()"
        expected_display = _flatten(test.expected_output)
        got_display = _got_display(grade_result)

        for col, text in enumerate((input_display, expected_display, got_display)):
            label = tk.Label(
                self.table_frame, text=text, font=_CELL_FONT, foreground=_TEXT_COLOR,
                background=_CELL_BG, padx=6, pady=2, anchor="w",
            )
            label.grid(row=row, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))

        mark = _PASS_MARK if grade_result.passed else _FAIL_MARK
        mark_color = _PASS_COLOR if grade_result.passed else _FAIL_COLOR
        ok_label = tk.Label(
            self.table_frame, text=mark, font=_CELL_FONT, foreground=mark_color,
            background=_CELL_BG, padx=6, pady=2, anchor="center",
        )
        ok_label.grid(row=row, column=3, sticky="nsew", padx=(0, 1), pady=(0, 1))


def _flatten(text: str) -> str:
    """Joins a multi-line string into one table-cell-friendly line.

    Args:
        text: The (possibly multi-line) text to flatten.

    Returns:
        The text's lines joined with " | ", or "(empty)" if there's
        nothing but whitespace.
    """
    lines = text.strip().splitlines()
    return " | ".join(lines) if lines else "(empty)"


def _got_display(grade_result) -> str:
    """Picks what to show in the "Got" column for one test result.

    Args:
        grade_result: The GradeResult to summarize.

    Returns:
        The student's actual output, flattened to one line - or, if
        there was none and the test failed, why: the timeout message,
        or just the exception line for a crash (its last line), rather
        than the full traceback, which wouldn't fit in a table cell.
    """
    actual = grade_result.actual_output.strip()
    if actual:
        return _flatten(actual)
    if not grade_result.passed:
        return grade_result.reason.strip().splitlines()[-1]
    return "(empty)"
