"""
File: main_window.py
Author: Bior Madol Khom Bior
----------------------------
The app's main window. On the left is a list of topics with their
problems underneath; on the right is the problem the student picked.
Clicking a problem, or pressing Next Problem, loads it on the right.
"""

import tkinter as tk
from tkinter import ttk

from core.problem_loader import ProblemLoader
from gui.problem_view import ProblemView

ACCENT_GREEN = "#2F6F4F"
ACCENT_GREEN_DARK = "#26593F"
ACCENT_GREEN_FADED = "#A9C4B5"
SIDEBAR_BACKGROUND = "#FAFAF8"
TEXT_COLOR = "#1A1A1A"

# Topic names that read badly when just capitalized.
TOPIC_LABELS = {"io": "I/O"}


def topic_label(topic_name: str) -> str:
    """Turns a topic name into a sidebar label: "loops" -> "Loops"."""
    if topic_name in TOPIC_LABELS:
        return TOPIC_LABELS[topic_name]
    return topic_name.replace("_", " ").title()


def row_id(topic_name: str, problem_id: str) -> str:
    """The sidebar row id for a problem, such as "loops::loops_001"."""
    return f"{topic_name}::{problem_id}"


class MainWindow(tk.Tk):

    def __init__(self, content_dir):
        """Loads every problem and builds the window."""
        super().__init__()
        self.title("Sudopy — Learn Python Offline")
        self.geometry("1000x650")
        self.minsize(800, 500)

        self.loader = ProblemLoader(content_dir)
        self.topics = self.loader.load_all()

        self._problem_rows = []         # every problem's row id, top to bottom
        self._current_row = None

        self._set_up_styles()
        self._build_layout()
        self._fill_sidebar()

    def _set_up_styles(self):
        """
        Sets the colors and fonts used by the sidebar and the green Run
        button. The "clam" theme is used because the built-in macOS theme
        ignores most custom colors.
        """
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Sidebar.Treeview", background=SIDEBAR_BACKGROUND,
                        fieldbackground=SIDEBAR_BACKGROUND, foreground=TEXT_COLOR,
                        rowheight=30, borderwidth=0, font=("TkDefaultFont", 11))
        style.map("Sidebar.Treeview",
                  background=[("selected", ACCENT_GREEN)],
                  foreground=[("selected", "white")])

        style.configure("Primary.TButton", background=ACCENT_GREEN, foreground="white",
                        font=("TkDefaultFont", 10, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", ACCENT_GREEN_DARK), ("disabled", ACCENT_GREEN_FADED)],
                  foreground=[("disabled", "#EFEFEF")])

    def _build_layout(self):
        """Places the sidebar on the left and the problem view on the right."""
        panes = ttk.Panedwindow(self, orient="horizontal")
        panes.pack(fill="both", expand=True)

        sidebar = ttk.Frame(panes, width=280)
        ttk.Label(sidebar, text="Problems", font=("TkDefaultFont", 12, "bold")).pack(
            anchor="w", padx=14, pady=(14, 8))
        self.tree = ttk.Treeview(sidebar, style="Sidebar.Treeview", show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 10))
        self.tree.tag_configure("topic", font=("TkDefaultFont", 11, "bold"))
        self.tree.bind("<<TreeviewSelect>>", self._on_row_selected)
        panes.add(sidebar, weight=0)

        right_side = ttk.Frame(panes, padding=18)
        self.problem_view = ProblemView(right_side, on_next=self._go_to_next_problem)
        self.problem_view.pack(fill="both", expand=True)
        panes.add(right_side, weight=1)

    def _fill_sidebar(self):
        """Adds a row for every topic, with its numbered problems under it, and selects the first problem."""
        for topic_name, topic in self.topics.items():
            self.tree.insert("", "end", iid=topic_name, text=topic_label(topic_name),
                             tags=("topic",), open=True)
            for number, problem in enumerate(topic.problems, start=1):
                problem_row = row_id(topic_name, problem.id)
                self._problem_rows.append(problem_row)
                self.tree.insert(topic_name, "end", iid=problem_row, text=f"{number}. {problem.title}")

        if self._problem_rows:
            self._select_row(self._problem_rows[0])

    def _select_row(self, row):
        """Selects a sidebar row, which loads it through _on_row_selected."""
        self.tree.selection_set(row)
        self.tree.see(row)

    def _on_row_selected(self, event):
        """
        Loads the selected problem. Clicking a topic row loads that topic's
        first problem, so clicking a topic is never a dead end.
        """
        selection = self.tree.selection()
        if not selection:
            return
        row = selection[0]

        if row in self.topics:
            topic_name = row
            problem = self.topics[topic_name].problems[0]
        else:
            topic_name, problem_id = row.split("::")
            problem = self.loader.get_problem(topic_name, problem_id)

        self._current_row = row_id(topic_name, problem.id)
        self.problem_view.load_problem(problem)
        is_last = self._current_row == self._problem_rows[-1]
        self.problem_view.set_next_enabled(not is_last)

    def _go_to_next_problem(self):
        """Selects the problem right after the current one."""
        if self._current_row is None:
            return
        index = self._problem_rows.index(self._current_row)
        if index + 1 < len(self._problem_rows):
            self._select_row(self._problem_rows[index + 1])
