"""
File: problem_view.py
Author: Bior Madol Khom Bior
----------------------------
Shows one problem: its title and prompt, a hint hidden behind a button,
the code editor, the buttons, and the test results.

Grading can take a few seconds (up to 5 for code stuck in an infinite
loop), so it runs on a separate thread. That keeps the window responsive
while "Running..." is shown. Tkinter widgets may only be touched from the
main thread, so the grading thread only computes the results; the main
thread checks every 100 ms whether they're ready and then displays them.

Show Solution stays disabled until the student has pressed Run at least
once on the current problem.
"""

import threading
import tkinter as tk
from tkinter import ttk

from core.submission import run_and_grade_all
from gui.code_editor import CodeEditor
from gui.results_view import ResultsView

CHECK_EVERY_MS = 100
HINT_COLOR = "#57606a"
CODE_FONT = ("Courier New", 11)


class ProblemView(ttk.Frame):

    def __init__(self, parent, on_next):
        """
        Builds the view with no problem loaded yet. on_next is called when
        Next Problem is pressed, since only the main window knows which
        problem comes next.
        """
        super().__init__(parent)
        self.problem = None
        self._on_next = on_next
        self._grading_thread = None
        self._grade_results = None

        self.title_label = ttk.Label(self, font=("TkDefaultFont", 14, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 4))
        self.prompt_label = ttk.Label(self, wraplength=700, justify="left")
        self.prompt_label.pack(anchor="w", pady=(0, 10))

        # The hint button and hint text are only placed on screen by load_problem and _show_hint.
        self.hint_button = ttk.Button(self, text="Show Hint", command=self._show_hint)
        self.hint_label = ttk.Label(self, wraplength=700, justify="left", foreground=HINT_COLOR)

        self.editor_frame = ttk.LabelFrame(self, text="Your code")
        self.editor_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.editor = CodeEditor(self.editor_frame, font=CODE_FONT)
        self.editor.pack(fill="both", expand=True, padx=4, pady=4)

        self._build_buttons()
        self.results_view = ResultsView(self)

    def _build_buttons(self):
        """Adds the Run, Reset, Show Solution and Next Problem buttons in one row."""
        row = ttk.Frame(self)
        row.pack(fill="x", pady=(0, 10))
        self.run_button = ttk.Button(row, text="Run", command=self._run, style="Primary.TButton")
        self.reset_button = ttk.Button(row, text="Reset to starter code", command=self._reset)
        self.solution_button = ttk.Button(row, text="Show Solution", command=self._show_solution)
        self.next_button = ttk.Button(row, text="Next Problem", command=self._on_next)

        self.run_button.pack(side="left")
        for button in (self.reset_button, self.solution_button, self.next_button):
            button.pack(side="left", padx=(8, 0))

    def load_problem(self, problem):
        """Shows a new problem with its starter code, its hint hidden, and no results."""
        self.problem = problem
        self.title_label.config(text=problem.title)
        self.prompt_label.config(text=problem.prompt)
        self.solution_button.config(state="disabled")

        self.hint_label.pack_forget()
        self.hint_button.pack_forget()
        if problem.hint:
            self.hint_button.pack(anchor="w", pady=(0, 10), before=self.editor_frame)

        self.editor.set_text(problem.starter_code)
        self.results_view.clear()

    def set_next_enabled(self, enabled: bool):
        """Turns the Next Problem button on or off (off on the very last problem)."""
        if enabled:
            self.next_button.config(state="normal")
        else:
            self.next_button.config(state="disabled")

    def _run(self):
        """Starts grading the student's code on a separate thread."""
        if self.problem is None or self._grading_thread is not None:
            return
        self.run_button.config(text="Running...", state="disabled")

        code = self.editor.get_text()
        problem = self.problem
        self._grade_results = None
        self._grading_thread = threading.Thread(
            target=self._grade_in_background, args=(code, problem), daemon=True)
        self._grading_thread.start()
        self.after(CHECK_EVERY_MS, self._check_if_graded, problem)

    def _grade_in_background(self, code, problem):
        """Runs on the grading thread. Grades the code and stores the results."""
        self._grade_results = run_and_grade_all(code, problem.function_name, problem.tests)

    def _check_if_graded(self, problem):
        """
        Runs on the main thread every 100 ms until grading is done, then shows
        the results. If the student switched problems meanwhile, the results
        belong to the old problem and are not shown.
        """
        if self._grading_thread.is_alive():
            self.after(CHECK_EVERY_MS, self._check_if_graded, problem)
            return

        self._grading_thread = None
        self.run_button.config(text="Run", state="normal")
        if problem is not self.problem:
            return
        self.results_view.show_results(problem.function_name, problem.tests, self._grade_results)
        self.solution_button.config(state="normal")

    def _show_hint(self):
        """Replaces the Show Hint button with the hint itself."""
        self.hint_button.pack_forget()
        self.hint_label.config(text=f"Hint: {self.problem.hint}")
        self.hint_label.pack(anchor="w", pady=(0, 10), before=self.editor_frame)

    def _show_solution(self):
        """Opens a small read-only window with the problem's solution."""
        window = tk.Toplevel(self)
        window.title(f"Solution — {self.problem.title}")
        window.geometry("500x400")

        text = tk.Text(window, wrap="none", font=CODE_FONT, padx=10, pady=10)
        text.pack(fill="both", expand=True)
        text.insert("1.0", self.problem.solution)
        text.config(state="disabled")
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=(0, 10))

    def _reset(self):
        """Throws away the student's changes and brings back the starter code."""
        if self.problem is None:
            return
        self.editor.set_text(self.problem.starter_code)
        self.results_view.clear()
