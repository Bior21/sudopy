"""Displays a single problem and lets the student run and grade their code.

Shows the prompt text, a Show Hint button that reveals the hint on
click, an editable code area pre-filled with starter_code, Run/Reset/
Show Solution/Next Problem buttons, and a ResultsView showing pass/fail
feedback. ProblemView wires directly to core.submission (and, through
it, core.runner and core.grader) when Run is clicked. Kept as a single
frame class for now; if it grows too large later, the editor pane can
be split out into its own file.

The Show Solution button stays disabled until the student has clicked
Run at least once for the currently loaded problem - passing, failing,
or a mix of both all count, the only thing gated on is having made a
genuine attempt first. Run uses the "Primary.TButton" style (see
gui/main_window.py's _configure_style) so it visually stands out from
the secondary Reset/Show Solution/Next Problem actions.

Next Problem is an alternative to clicking a row in the navigation
tree, not a replacement for it - ProblemView itself has no notion of
problem ordering, so it just calls the on_next callback MainWindow
supplies and lets MainWindow (which owns the tree) figure out what
"next" means.
"""

import tkinter as tk
from tkinter import ttk

from core.solutions import SOLUTIONS
from core.submission import run_and_grade_all
from gui.results_view import ResultsView
from gui.code_editor import CodeEditor


class ProblemView(ttk.Frame):
    def __init__(self, parent, on_next=None):
        """Builds the prompt/editor/results layout, with no problem loaded yet.

        Args:
            parent: The Tkinter widget this frame is placed inside.
            on_next: Optional callback invoked when the Next Problem
                button is clicked. ProblemView has no notion of problem
                ordering, so it just delegates to the caller.
        """
        super().__init__(parent)
        self.current_problem = None
        self._has_attempted_current_problem = False
        self._on_next = on_next

        # Prompt
        self.title_label = ttk.Label(self, text="", font=("TkDefaultFont", 14, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 4))

        self.prompt_label = ttk.Label(self, text="", wraplength=700, justify="left")
        self.prompt_label.pack(anchor="w", pady=(0, 10))

        # Hint - hidden behind a button until clicked (see _on_show_hint).
        # Neither widget is packed here; load_problem() shows hint_button
        # only when the problem actually has a hint.
        self.hint_button = ttk.Button(self, text="Show Hint", command=self._on_show_hint)
        self.hint_label = ttk.Label(
            self, text="", wraplength=700, justify="left", foreground="#57606a"
        )

        # Code editor
        self.editor_frame = ttk.LabelFrame(self, text="Your code")
        self.editor_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.editor = CodeEditor(self.editor_frame, font=("Courier New", 11))
        self.editor.pack(fill="both", expand=True, padx=4, pady=4)

        # Run button
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=(0, 10))
        self.run_button = ttk.Button(
            button_frame, text="Run", command=self._on_run, style="Primary.TButton"
        )
        self.run_button.pack(side="left")
        self.reset_button = ttk.Button(button_frame, text="Reset to starter code", command=self._on_reset)
        self.reset_button.pack(side="left", padx=(8, 0))
        self.show_solution_button = ttk.Button(
            button_frame, text="Show Solution", command=self._on_show_solution, state="disabled"
        )
        self.show_solution_button.pack(side="left", padx=(8, 0))
        self.next_button = ttk.Button(
            button_frame, text="Next Problem", command=self._on_next_clicked
        )
        self.next_button.pack(side="left", padx=(8, 0))

        # Results - stays hidden (see ResultsView.clear()) until the
        # student's code has actually been run
        self.results_view = ResultsView(self)

    def load_problem(self, problem):
        """Displays the given problem: prompt, starter code, cleared results.

        The hint (if any) starts hidden behind the Show Hint button -
        see _on_show_hint.

        Args:
            problem: The core.problem_loader.Problem to display.
        """
        self.current_problem = problem
        self._has_attempted_current_problem = False
        self.show_solution_button.config(state="disabled")
        self.title_label.config(text=problem.title)
        self.prompt_label.config(text=problem.prompt)

        self.hint_button.pack_forget()
        self.hint_label.pack_forget()
        self.hint_label.config(text="")
        if problem.hint:
            self.hint_button.pack(anchor="w", pady=(0, 10), before=self.editor_frame)

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
        self.results_view.update_results(
            self.current_problem.function_name, self.current_problem.tests, grade_results
        )

        self._has_attempted_current_problem = True
        self.show_solution_button.config(state="normal")

    def _on_show_hint(self):
        """Reveals the current problem's hint, replacing the button with the text."""
        if not self.current_problem:
            return
        self.hint_label.config(text=f"Hint: {self.current_problem.hint}")
        self.hint_button.pack_forget()
        self.hint_label.pack(anchor="w", pady=(0, 10), before=self.editor_frame)

    def _on_show_solution(self):
        """Opens a read-only window showing the current problem's reference solution.

        Only reachable once the Show Solution button is enabled, which
        happens after the student has clicked Run at least once for this
        problem (see _on_run).
        """
        if not self.current_problem or not self._has_attempted_current_problem:
            return
        solution = SOLUTIONS.get(self.current_problem.id)
        if solution is None:
            return

        window = tk.Toplevel(self)
        window.title(f"Solution — {self.current_problem.title}")
        window.geometry("500x400")

        text = tk.Text(window, wrap="none", font=("Courier New", 11), padx=10, pady=10)
        text.pack(fill="both", expand=True)
        text.insert("1.0", solution)
        text.config(state="disabled")

        ttk.Button(window, text="Close", command=window.destroy).pack(pady=(0, 10))

    def _on_next_clicked(self):
        """Delegates to the on_next callback, if one was supplied."""
        if self._on_next:
            self._on_next()

    def set_next_enabled(self, enabled: bool):
        """Enables or disables the Next Problem button.

        Args:
            enabled: False when the currently loaded problem is the last
                one in the whole curriculum, so there's nowhere to go.
        """
        self.next_button.config(state="normal" if enabled else "disabled")

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
