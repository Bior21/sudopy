"""
File: results_view.py
Author: Bior Madol Khom Bior
----------------------------
Shows how the student's code did: a summary line such as "2/3 test(s)
passed" and a table with one row per test, listing the call that was
made, the expected output, what the code printed, and a ✓ or ✗. The
whole panel stays hidden until the student first presses Run.
"""

import tkinter as tk
from tkinter import ttk

PASS_COLOR = "#1a7f37"
FAIL_COLOR = "#cf222e"
BORDER_COLOR = "#D0D0D0"
HEADER_BACKGROUND = "#EFEFEF"
TEXT_COLOR = "#1A1A1A"
HEADER_FONT = ("TkDefaultFont", 9, "bold")
CELL_FONT = ("TkDefaultFont", 9)
COLUMN_TITLES = ["Input / Call", "Expected", "Got", "OK"]


class ResultsView(ttk.Frame):

    def __init__(self, parent):
        """Builds the summary line and the table's header row, hidden for now."""
        super().__init__(parent)
        self.summary_label = ttk.Label(self, font=("TkDefaultFont", 11, "bold"))
        self.summary_label.pack(anchor="w", pady=(0, 6))

        # The table's background is the border color. Each cell leaves a 1px
        # gap around itself, and the background shows through as grid lines.
        self.table = tk.Frame(self, background=BORDER_COLOR)
        self.table.pack(fill="x")
        for column in range(3):
            self.table.grid_columnconfigure(column, weight=1)

        for column, title in enumerate(COLUMN_TITLES):
            self._add_cell(0, column, title, HEADER_FONT, TEXT_COLOR, HEADER_BACKGROUND)

    def clear(self):
        """Hides the panel until the next run."""
        self.pack_forget()

    def show_results(self, function_name, tests, grade_results):
        """Fills in the summary and one table row per test, then shows the panel."""
        self._show_summary(grade_results)
        self._remove_rows()
        row = 1
        for test, result in zip(tests, grade_results):
            self._add_row(row, function_name, test, result)
            row += 1
        self.pack(fill="x")

    def _show_summary(self, grade_results):
        """Sets the summary line, in green if every test passed and red if not."""
        passed = 0
        for result in grade_results:
            if result.passed:
                passed += 1
        total = len(grade_results)
        if passed == total:
            self.summary_label.config(text=f"All {total} test(s) passed!", foreground=PASS_COLOR)
        else:
            self.summary_label.config(text=f"{passed}/{total} test(s) passed", foreground=FAIL_COLOR)

    def _remove_rows(self):
        """Removes every row except the header row."""
        for cell in self.table.grid_slaves():
            if int(cell.grid_info()["row"]) != 0:
                cell.destroy()

    def _add_row(self, row, function_name, test, result):
        """Adds one test's row to the table."""
        self._add_cell(row, 0, call_text(function_name, test))
        self._add_cell(row, 1, one_line(test.expected_output))
        self._add_cell(row, 2, got_text(result))
        if result.passed:
            self._add_cell(row, 3, "✓", color=PASS_COLOR)
        else:
            self._add_cell(row, 3, "✗", color=FAIL_COLOR)

    def _add_cell(self, row, column, text, font=CELL_FONT, color=TEXT_COLOR, background="white"):
        """Places one cell of text in the table."""
        cell = tk.Label(self.table, text=text, font=font, foreground=color,
                        background=background, padx=6, pady=2, anchor="w")
        cell.grid(row=row, column=column, sticky="nsew", padx=(0, 1), pady=(0, 1))


def call_text(function_name, test) -> str:
    """
    What to show in the "Input / Call" column: the function call when the
    test passes arguments, such as "add(2, 3)", or else the typed input.
    """
    if test.args:
        arg_texts = []
        for arg in test.args:
            arg_texts.append(repr(arg))
        return f"{function_name}({', '.join(arg_texts)})"
    if test.input.strip():
        return one_line(test.input)
    return f"{function_name}()"


def one_line(text: str) -> str:
    """Joins several lines with " | " so they fit in one cell."""
    lines = text.strip().splitlines()
    if not lines:
        return "(empty)"
    return " | ".join(lines)


def got_text(result) -> str:
    """
    What to show in the "Got" column: what the code printed. If it printed
    nothing and failed, the last line of the reason instead, which for a
    crash is the error itself, such as "ZeroDivisionError: division by zero".
    """
    if result.actual_output.strip():
        return one_line(result.actual_output)
    if not result.passed:
        return result.reason.strip().splitlines()[-1]
    return "(empty)"
