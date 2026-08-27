"""A self-contained code editor widget for the problem view.

Provides a line-number gutter with synced scrolling, lightweight
regex-based Python syntax highlighting, current-line highlighting, and
Tab-inserts-4-spaces - the baseline things that make a text box read as
"a code editor" rather than a plain text field. It's deliberately not a
full tokenizer/parser: regex-based highlighting can be fooled by edge
cases (e.g. a '#' inside a string that isn't a comment), which is
acceptable here since this is a teaching tool for beginner-level code,
not a production IDE, and the tradeoff keeps this file small and
dependency-free. CodeEditor exposes get/delete/insert proxied to the
underlying Text widget, so it can be dropped in wherever a plain tk.Text
was used for the editor without changing the calling code.
"""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import ttk

PY_KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield",
}

PY_BUILTINS = {
    "print", "input", "int", "float", "str", "bool", "list", "dict",
    "tuple", "set", "len", "range", "sum", "max", "min", "sorted",
    "enumerate", "zip", "abs", "round", "type", "open", "map", "filter",
}

# Order matters: string/comment are re-raised above keyword/builtin/number
# afterward so a keyword-looking substring inside a string or comment
# still displays as a string/comment, not a keyword.
_TOKEN_PATTERNS = [
    ("number", r"\b\d+(\.\d+)?\b"),
    ("keyword", r"\b(?:" + "|".join(sorted(PY_KEYWORDS)) + r")\b"),
    ("builtin", r"\b(?:" + "|".join(sorted(PY_BUILTINS)) + r")\b"),
    ("string", r"(\"\"\".*?\"\"\"|'''.*?'''|\"[^\"\n]*\"|'[^'\n]*')"),
    ("comment", r"#.*"),
]

_COLORS = {
    "keyword": "#0057B7",
    "builtin": "#7A3E9D",
    "string": "#0B7A3E",
    "comment": "#8A8A8A",
    "number": "#B15C00",
}


class CodeEditor(ttk.Frame):
    def __init__(self, parent, font=("Courier New", 11)):
        """Builds the line-number gutter and text area, and wires up highlighting.

        Args:
            parent: The Tkinter widget this frame is placed inside.
            font: The font tuple used for both the gutter and the text area.
        """
        super().__init__(parent)
        self._font = font

        self.linenumbers = tk.Text(
            self,
            width=4,
            padx=6,
            pady=4,
            takefocus=0,
            border=0,
            background="#EAEAEA",
            foreground="#8A8A8A",
            state="disabled",
            font=font,
            wrap="none",
        )
        self.linenumbers.pack(side="left", fill="y")

        self.text = tk.Text(
            self,
            wrap="none",
            font=font,
            padx=6,
            pady=4,
            undo=True,
            background="white",
            foreground="#1A1A1A",
            insertbackground="black",
            border=0,
        )
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._on_scroll)
        scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self._on_text_scroll(scrollbar))

        self.text.tag_configure("currentline", background="#F3F3F3")
        for tag, color in _COLORS.items():
            self.text.tag_configure(tag, foreground=color)

        self.text.bind("<KeyRelease>", self._on_change)
        self.text.bind("<ButtonRelease>", self._on_change)
        self.text.bind("<Tab>", self._on_tab)

        self._refresh()

    # --- scrolling: keep gutter and editor in lockstep ---

    def _on_scroll(self, *args):
        """Scrolls both the editor and the line-number gutter together.

        Args:
            *args: The scroll command arguments Tkinter passes to a
                yscrollcommand handler.
        """
        self.text.yview(*args)
        self.linenumbers.yview(*args)

    def _on_text_scroll(self, scrollbar):
        """Builds the callback that keeps the scrollbar and gutter in sync.

        The returned handler runs whenever the text widget scrolls on its
        own, such as while typing past the visible area.

        Args:
            scrollbar: The scrollbar widget to update.

        Returns:
            A callback suitable for use as the text widget's yscrollcommand.
        """
        def handler(first, last):
            scrollbar.set(first, last)
            self.linenumbers.yview_moveto(first)
        return handler

    # --- editing behavior ---

    def _on_tab(self, event):
        """Inserts 4 spaces instead of a literal tab character.

        Args:
            event: The Tkinter key event that triggered this handler.

        Returns:
            The string "break", which tells Tkinter to skip its default
            Tab behavior of shifting focus to the next widget.
        """
        self.text.insert("insert", "    ")
        return "break"  # prevent default focus-shift behavior

    def _on_change(self, event=None):
        """Re-renders line numbers and highlighting after an edit.

        Args:
            event: The Tkinter event that triggered this handler. Unused.
        """
        self._refresh()

    def _refresh(self):
        """Recomputes line numbers, syntax highlighting, and the current-line marker."""
        self._update_line_numbers()
        self._highlight_syntax()
        self._highlight_current_line()

    def _update_line_numbers(self):
        """Redraws the gutter to match the editor's current line count."""
        line_count = int(self.text.index("end-1c").split(".")[0])
        numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))

        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", "end")
        self.linenumbers.insert("1.0", numbers_text)
        self.linenumbers.config(state="disabled")

    def _highlight_syntax(self):
        """Re-tags every keyword/builtin/string/comment/number match in the text."""
        for tag in _COLORS:
            self.text.tag_remove(tag, "1.0", "end")

        content = self.text.get("1.0", "end-1c")
        for tag, pattern in _TOKEN_PATTERNS:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text.tag_add(tag, start, end)

        # strings/comments should visually win over keyword/builtin/number
        # matches that happen to fall inside them
        self.text.tag_raise("string")
        self.text.tag_raise("comment")

    def _highlight_current_line(self):
        """Shades the line the cursor is currently on."""
        self.text.tag_remove("currentline", "1.0", "end")
        self.text.tag_add("currentline", "insert linestart", "insert lineend+1c")

    # --- proxy interface so callers can treat this like a plain tk.Text ---

    def get(self, *args, **kwargs):
        """Proxies to the underlying Text widget's get().

        Args:
            *args: Positional arguments forwarded to Text.get().
            **kwargs: Keyword arguments forwarded to Text.get().

        Returns:
            The requested text.
        """
        return self.text.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Proxies to the underlying Text widget's delete().

        Args:
            *args: Positional arguments forwarded to Text.delete().
            **kwargs: Keyword arguments forwarded to Text.delete().
        """
        self.text.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        """Proxies to the underlying Text widget's insert(), then re-renders.

        Args:
            *args: Positional arguments forwarded to Text.insert().
            **kwargs: Keyword arguments forwarded to Text.insert().
        """
        self.text.insert(*args, **kwargs)
        self._refresh()

    def focus_set(self):
        """Moves keyboard focus to the underlying Text widget."""
        self.text.focus_set()
