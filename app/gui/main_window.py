"""The top-level application window.

Lays out three panes side by side: a topic sidebar, a problem list, and
the problem view (prompt/editor/results). MainWindow owns the
ProblemLoader and drives which Problem is currently loaded into the
ProblemView based on the user's sidebar and list selections.
"""

import tkinter as tk
from tkinter import ttk

from core.problem_loader import ProblemLoader
from gui.problem_view import ProblemView


class MainWindow(tk.Tk):
    def __init__(self, content_dir):
        """Builds the window and loads all topics/problems.

        Args:
            content_dir: Path to the directory containing problem content.
        """
        super().__init__()
        self.title("Sudopy — Learn Python Offline")
        self.geometry("1000x650")
        self.minsize(800, 500)

        self.loader = ProblemLoader(content_dir)
        self.topics = self.loader.load_all()

        self._build_layout()
        self._populate_topics()

    def _build_layout(self):
        """Builds the three-pane layout: topic sidebar, problem list, problem view."""
        # Use a horizontal paned window so users can resize panels
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # --- Topic sidebar ---
        topic_frame = ttk.Frame(paned, width=180)
        ttk.Label(topic_frame, text="Topics", font=("TkDefaultFont", 11, "bold")).pack(
            anchor="w", padx=6, pady=(6, 2)
        )
        self.topic_listbox = tk.Listbox(topic_frame, exportselection=False)
        self.topic_listbox.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.topic_listbox.bind("<<ListboxSelect>>", self._on_topic_selected)
        paned.add(topic_frame, weight=0)

        # --- Problem list ---
        problem_frame = ttk.Frame(paned, width=220)
        ttk.Label(problem_frame, text="Problems", font=("TkDefaultFont", 11, "bold")).pack(
            anchor="w", padx=6, pady=(6, 2)
        )
        self.problem_listbox = tk.Listbox(problem_frame, exportselection=False)
        self.problem_listbox.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.problem_listbox.bind("<<ListboxSelect>>", self._on_problem_selected)
        paned.add(problem_frame, weight=0)

        # --- Problem view (prompt/editor/results) ---
        view_container = ttk.Frame(paned, padding=10)
        self.problem_view = ProblemView(view_container)
        self.problem_view.pack(fill="both", expand=True)
        paned.add(view_container, weight=1)

        self._current_topic_name = None

    def _populate_topics(self):
        """Fills the topic sidebar and loads the first topic by default."""
        self.topic_listbox.delete(0, "end")
        for topic_name in self.topics.keys():
            self.topic_listbox.insert("end", topic_name)
        if self.topics:
            self.topic_listbox.selection_set(0)
            self._load_topic(list(self.topics.keys())[0])

    def _on_topic_selected(self, event):
        """Handles a click in the topic sidebar.

        Args:
            event: The Tkinter listbox selection event. Unused; the
                current selection is read directly from the listbox.
        """
        selection = self.topic_listbox.curselection()
        if not selection:
            return
        topic_name = self.topic_listbox.get(selection[0])
        self._load_topic(topic_name)

    def _load_topic(self, topic_name):
        """Fills the problem list for a topic and loads its first problem.

        Args:
            topic_name: The name of the topic to display.
        """
        self._current_topic_name = topic_name
        topic = self.loader.get_topic(topic_name)
        self.problem_listbox.delete(0, "end")
        for problem in topic.problems:
            self.problem_listbox.insert("end", problem.title)
        if topic.problems:
            self.problem_listbox.selection_set(0)
            self.problem_view.load_problem(topic.problems[0])

    def _on_problem_selected(self, event):
        """Handles a click in the problem list.

        Args:
            event: The Tkinter listbox selection event. Unused; the
                current selection is read directly from the listbox.
        """
        selection = self.problem_listbox.curselection()
        if not selection or not self._current_topic_name:
            return
        topic = self.loader.get_topic(self._current_topic_name)
        problem = topic.problems[selection[0]]
        self.problem_view.load_problem(problem)
