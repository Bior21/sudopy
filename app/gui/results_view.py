"""Displays the outcome of running and grading a student's code.

Shows pass/fail status, the reason, and actual vs expected output for
debugging. ResultsView is deliberately dumb and stateless - it just
renders whatever GradeResult it's given via update_result(), with no
knowledge of runner/grader internals beyond the GradeResult shape.
"""

import tkinter as tk
from tkinter import ttk


class ResultsView(ttk.Frame):
    def __init__(self, parent):
        """Builds the pass/fail status, reason, and actual/expected output panes.

        Args:
            parent: The Tkinter widget this frame is placed inside.
        """
        super().__init__(parent)

        self.status_label = ttk.Label(
            self, text="Run your code to see results here.", font=("TkDefaultFont", 11, "bold")
        )
        self.status_label.pack(anchor="w", pady=(0, 6))

        self.reason_label = ttk.Label(self, text="", wraplength=500, justify="left")
        self.reason_label.pack(anchor="w", pady=(0, 6))

        output_frame = ttk.Frame(self)
        output_frame.pack(fill="both", expand=True)

        actual_frame = ttk.LabelFrame(output_frame, text="Your output")
        actual_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self.actual_text = tk.Text(actual_frame, height=6, state="disabled", wrap="word")
        self.actual_text.pack(fill="both", expand=True)

        expected_frame = ttk.LabelFrame(output_frame, text="Expected output")
        expected_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))
        self.expected_text = tk.Text(expected_frame, height=6, state="disabled", wrap="word")
        self.expected_text.pack(fill="both", expand=True)

    def clear(self):
        """Resets the view to its initial "no result yet" state."""
        self.status_label.config(text="Run your code to see results here.", foreground="black")
        self.reason_label.config(text="")
        self._set_text(self.actual_text, "")
        self._set_text(self.expected_text, "")

    def update_result(self, grade_result):
        """Renders a grading result: status, reason, and actual vs expected output.

        Args:
            grade_result: The core.grader.GradeResult to display.
        """
        if grade_result.passed:
            self.status_label.config(text="PASSED", foreground="#1a7f37")
        else:
            self.status_label.config(text="NOT PASSED", foreground="#cf222e")

        self.reason_label.config(text=grade_result.reason)
        self._set_text(self.actual_text, grade_result.actual_output)
        self._set_text(self.expected_text, grade_result.expected_output)

    @staticmethod
    def _set_text(widget: tk.Text, content: str):
        """Replaces a read-only Text widget's contents.

        Args:
            widget: The (normally disabled) Text widget to update.
            content: The text to display.
        """
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="disabled")
