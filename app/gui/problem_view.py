"""Displays a single problem and lets the student run and grade their code.

Shows the prompt text, an editable code area pre-filled with
starter_code, a Run button, and a ResultsView showing pass/fail feedback.
ProblemView wires directly to core.submission (and, through it,
core.runner and core.grader) when Run is clicked. Kept as a single frame
class for now; if it grows too large later, the editor pane can be split
out into its own file.
"""

import tkinter as tk
from tkinter import ttk

from core.submission import run_and_grade_all
from gui.results_view import ResultsView
from gui.code_editor import CodeEditor


class ProblemView(ttk.Frame):
    def __init__(self, parent):
        """Builds the prompt/editor/results layout, with no problem loaded yet.

        Args:
            parent: The Tkinter widget this frame is placed inside.
        """
        super().__init__(parent)
        self.current_problem = None

        # Prompt
        self.title_label = ttk.Label(self, text="", font=("TkDefaultFont", 14, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 4))

        self.prompt_label = ttk.Label(self, text="", wraplength=700, justify="left")
        self.prompt_label.pack(anchor="w", pady=(0, 10))

        # Hint (collapsed by default via a button toggle - simple v1: just show it)
        self.hint_label = ttk.Label(
            self, text="", wraplength=700, justify="left", foreground="#57606a"
        )
        self.hint_label.pack(anchor="w", pady=(0, 10))

        # Code editor
        editor_frame = ttk.LabelFrame(self, text="Your code")
        editor_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.editor = CodeEditor(editor_frame, font=("Courier New", 11))
        self.editor.pack(fill="both", expand=True, padx=4, pady=4)

        # Run button
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=(0, 10))
        self.run_button = ttk.Button(button_frame, text="Run", command=self._on_run)
        self.run_button.pack(side="left")
        self.reset_button = ttk.Button(button_frame, text="Reset to starter code", command=self._on_reset)
        self.reset_button.pack(side="left", padx=(8, 0))

        # Results
        self.results_view = ResultsView(self)
        self.results_view.pack(fill="both", expand=True)

    def load_problem(self, problem):
        """Displays the given problem: prompt, hint, starter code, cleared results.

        Args:
            problem: The core.problem_loader.Problem to display.
        """
        self.current_problem = problem
        self.title_label.config(text=problem.title)
        self.prompt_label.config(text=problem.prompt)
        self.hint_label.config(text=f"Hint: {problem.hint}" if problem.hint else "")
        self._set_editor_text(problem.starter_code)
        self.results_view.clear()

    def _on_run(self):
        """Runs and grades the student's current code against every test, then shows the results."""
        if not self.current_problem:
            return
        code = self.editor.get("1.0", "end-1c")
        grade_results = run_and_grade_all(
            code,
            self.current_problem.function_name,
            self.current_problem.tests,
        )
        self.results_view.update_results(self.current_problem.tests, grade_results)

    def _on_reset(self):
        """Discards the student's edits and restores the starter code."""
        if not self.current_problem:
            return
        self._set_editor_text(self.current_problem.starter_code)
        self.results_view.clear()

    def _set_editor_text(self, text: str):
        """Replaces the editor's contents.

        Args:
            text: The text to place in the editor.
        """
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", text)
