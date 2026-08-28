"""Displays the outcome of running and grading a student's code.

Shows an overall "X/Y tests passed" summary plus one row per test case,
each showing the input that was used and how the student's output
compared to what was expected. ResultsView is deliberately dumb and
stateless - it just renders whatever TestCase/GradeResult pairs it's
given via update_results(), with no knowledge of runner/grader internals
beyond the GradeResult shape.
"""

from tkinter import ttk

_PASS_COLOR = "#1a7f37"
_FAIL_COLOR = "#cf222e"


class ResultsView(ttk.Frame):
    def __init__(self, parent):
        """Builds the summary label and the (initially empty) per-test rows.

        Args:
            parent: The Tkinter widget this frame is placed inside.
        """
        super().__init__(parent)

        self.status_label = ttk.Label(
            self, text="Run your code to see results here.", font=("TkDefaultFont", 11, "bold")
        )
        self.status_label.pack(anchor="w", pady=(0, 8))

        self.tests_container = ttk.Frame(self)
        self.tests_container.pack(fill="both", expand=True)

    def clear(self):
        """Resets the view to its initial "no result yet" state."""
        self.status_label.config(text="Run your code to see results here.", foreground="black")
        self._clear_test_rows()

    def update_results(self, tests, grade_results):
        """Renders one row per test case, plus an overall pass/fail summary.

        Args:
            tests: The problem's core.problem_loader.TestCase list that
                was run, in the same order as grade_results.
            grade_results: The core.grader.GradeResult produced for each
                test in tests.
        """
        self._update_summary(grade_results)
        self._clear_test_rows()
        for index, (test, grade_result) in enumerate(zip(tests, grade_results), start=1):
            self._add_test_row(index, test, grade_result)

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

    def _clear_test_rows(self):
        """Removes every per-test row currently displayed."""
        for child in self.tests_container.winfo_children():
            child.destroy()

    def _add_test_row(self, index, test, grade_result):
        """Adds one test's result row: pass gets a one-liner, fail gets full detail.

        Args:
            index: The test's 1-based position, for display (e.g. "Test 2").
            test: The core.problem_loader.TestCase that was run.
            grade_result: The GradeResult produced by grading it.
        """
        row = ttk.Frame(self.tests_container)
        row.pack(fill="x", anchor="w", pady=(0, 6))

        input_display = test.input if test.input.strip() else "(no input)"
        status_text = "PASS" if grade_result.passed else "FAIL"
        status_color = _PASS_COLOR if grade_result.passed else _FAIL_COLOR

        if grade_result.passed:
            summary = (
                f"Test {index}: {status_text} — input: {input_display} "
                f"→ output: {grade_result.actual_output.strip()}"
            )
            ttk.Label(row, text=summary, foreground=status_color, wraplength=650, justify="left").pack(
                anchor="w"
            )
            return

        header = ttk.Label(
            row,
            text=f"Test {index}: {status_text} — input: {input_display}",
            font=("TkDefaultFont", 10, "bold"),
            foreground=status_color,
        )
        header.pack(anchor="w")

        detail_text = (
            f"{grade_result.reason}\n"
            f"your output:      {grade_result.actual_output.strip() or '(empty)'}\n"
            f"expected output:  {grade_result.expected_output.strip() or '(empty)'}"
        )
        detail = ttk.Label(row, text=detail_text, wraplength=650, justify="left", foreground="#3a3a3a")
        detail.pack(anchor="w", padx=(14, 0))
