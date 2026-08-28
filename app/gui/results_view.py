"""Displays the outcome of running and grading a student's code.

Shows an overall "X/Y tests passed" summary plus a table with one row
per test case: the input used (or the function call, for a test that
takes no input), the expected output, what the student's code actually
produced, and a pass/fail mark. ResultsView is deliberately dumb and
stateless - it just renders whatever it's given via update_results(),
with no knowledge of runner/grader internals beyond the GradeResult shape.
"""

from tkinter import ttk

_PASS_COLOR = "#1a7f37"
_FAIL_COLOR = "#cf222e"
_PASS_MARK = "✓"
_FAIL_MARK = "✗"

_COLUMNS = ("input", "expected", "got", "ok")


class ResultsView(ttk.Frame):
    def __init__(self, parent):
        """Builds the summary label and the (initially empty) results table.

        Args:
            parent: The Tkinter widget this frame is placed inside.
        """
        super().__init__(parent)

        self.status_label = ttk.Label(
            self, text="Run your code to see results here.", font=("TkDefaultFont", 11, "bold")
        )
        self.status_label.pack(anchor="w", pady=(0, 8))

        self.table = ttk.Treeview(self, columns=_COLUMNS, show="headings", height=6)
        self.table.heading("input", text="Input / Call")
        self.table.heading("expected", text="Expected")
        self.table.heading("got", text="Got")
        self.table.heading("ok", text="OK")
        self.table.column("input", width=160, anchor="w")
        self.table.column("expected", width=180, anchor="w")
        self.table.column("got", width=180, anchor="w")
        self.table.column("ok", width=50, anchor="center")
        self.table.pack(fill="both", expand=True)

        self.table.tag_configure("passed", foreground=_PASS_COLOR)
        self.table.tag_configure("failed", foreground=_FAIL_COLOR)

    def clear(self):
        """Resets the view to its initial "no result yet" state."""
        self.status_label.config(text="Run your code to see results here.", foreground="black")
        self.table.delete(*self.table.get_children())

    def update_results(self, function_name, tests, grade_results):
        """Fills the table with one row per test case, plus an overall summary.

        Args:
            function_name: The problem's function name, shown in the
                "Input / Call" column for a test that takes no input.
            tests: The problem's core.problem_loader.TestCase list that
                was run, in the same order as grade_results.
            grade_results: The core.grader.GradeResult produced for each
                test in tests.
        """
        self._update_summary(grade_results)
        self.table.delete(*self.table.get_children())
        for test, grade_result in zip(tests, grade_results):
            self._add_row(function_name, test, grade_result)

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

    def _add_row(self, function_name, test, grade_result):
        """Adds one test's row to the results table.

        Args:
            function_name: The problem's function name, used as the
                "Input / Call" cell when the test has no input.
            test: The core.problem_loader.TestCase that was run.
            grade_result: The GradeResult produced by grading it.
        """
        input_display = _flatten(test.input) if test.input.strip() else f"{function_name}()"
        expected_display = _flatten(test.expected_output)
        got_display = _got_display(grade_result)
        mark = _PASS_MARK if grade_result.passed else _FAIL_MARK
        tag = "passed" if grade_result.passed else "failed"

        self.table.insert(
            "", "end",
            values=(input_display, expected_display, got_display, mark),
            tags=(tag,),
        )


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
