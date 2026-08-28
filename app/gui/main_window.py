"""The top-level application window.

Lays out two panes side by side: a navigation tree listing every topic
with its problems nested underneath, and the problem view (prompt/editor/
results). MainWindow owns the ProblemLoader and drives which Problem is
currently loaded into the ProblemView based on the user's tree selection.
"""

import tkinter as tk
from tkinter import ttk

from core.problem_loader import ProblemLoader
from gui.problem_view import ProblemView

_TOPIC_DISPLAY_NAMES = {
    "io": "I/O",
}


def _display_topic_name(topic_name: str) -> str:
    """Turns a raw topic name like "nested" into a readable label.

    Args:
        topic_name: The topic's internal name, from ProblemLoader.

    Returns:
        A title-cased label, with a few short names (e.g. "io") spelled
        out by hand since title-casing alone reads oddly for them.
    """
    return _TOPIC_DISPLAY_NAMES.get(topic_name, topic_name.replace("_", " ").title())


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

        # Maps a problem row's tree item id to (topic_name, problem_id),
        # so a topic row (not in this map) can be told apart from a
        # problem row on selection.
        self._problem_by_iid: dict[str, tuple[str, str]] = {}

        self._configure_style()
        self._build_layout()
        self._populate_tree()

    def _configure_style(self):
        """Sets up a readable, consistent look for the navigation tree.

        Switches to the "clam" ttk theme, since the platform-native theme
        (e.g. aqua on macOS) ignores most custom Treeview colors, then
        applies a taller row height, a soft background, and a clear
        selection highlight so the tree reads as distinct rows rather
        than a run of plain text.
        """
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Sidebar.Treeview",
            background="#FAFAF8",
            fieldbackground="#FAFAF8",
            foreground="#1A1A1A",
            rowheight=30,
            borderwidth=0,
            relief="flat",
            font=("TkDefaultFont", 11),
        )
        style.map(
            "Sidebar.Treeview",
            background=[("selected", "#2F6F4F")],
            foreground=[("selected", "#FFFFFF")],
        )

    def _build_layout(self):
        """Builds the two-pane layout: the navigation tree and the problem view."""
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # --- Topic/problem navigation tree ---
        nav_frame = ttk.Frame(paned, width=280)
        ttk.Label(
            nav_frame, text="Problems", font=("TkDefaultFont", 12, "bold")
        ).pack(anchor="w", padx=14, pady=(14, 8))

        self.tree = ttk.Treeview(
            nav_frame, style="Sidebar.Treeview", show="tree", selectmode="browse"
        )
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 10))
        self.tree.tag_configure("topic", font=("TkDefaultFont", 11, "bold"))
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_selected)
        paned.add(nav_frame, weight=0)

        # --- Problem view (prompt/editor/results) ---
        view_container = ttk.Frame(paned, padding=18)
        self.problem_view = ProblemView(view_container)
        self.problem_view.pack(fill="both", expand=True)
        paned.add(view_container, weight=1)

    def _populate_tree(self):
        """Fills the tree with every topic and its problems.

        Each topic becomes an expanded parent row; its problems become
        numbered child rows underneath. The first problem of the first
        topic is selected and loaded by default.
        """
        first_problem_iid = None

        for topic_name, topic in self.topics.items():
            self.tree.insert(
                "", "end", iid=topic_name,
                text=_display_topic_name(topic_name),
                tags=("topic",), open=True,
            )
            for index, problem in enumerate(topic.problems, start=1):
                problem_iid = f"{topic_name}::{problem.id}"
                self._problem_by_iid[problem_iid] = (topic_name, problem.id)
                self.tree.insert(
                    topic_name, "end", iid=problem_iid,
                    text=f"{index}. {problem.title}",
                )
                if first_problem_iid is None:
                    first_problem_iid = problem_iid

        if first_problem_iid is not None:
            self.tree.selection_set(first_problem_iid)
            self.tree.see(first_problem_iid)

    def _on_tree_selected(self, event):
        """Loads the selected problem into the problem view.

        Selecting a topic row loads that topic's first problem instead,
        so clicking a section header is never a dead end.

        Args:
            event: The Tkinter Treeview selection event. Unused; the
                current selection is read directly from the tree.
        """
        selection = self.tree.selection()
        if not selection:
            return
        iid = selection[0]

        if iid in self._problem_by_iid:
            topic_name, problem_id = self._problem_by_iid[iid]
            problem = self.loader.get_problem(topic_name, problem_id)
        else:
            problem = self.loader.get_topic(iid).problems[0]

        self.problem_view.load_problem(problem)
