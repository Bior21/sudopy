"""
File: code_editor.py
Author: Bior Madol Khom Bior
----------------------------
A small code editor: a text box with line numbers, Python colors, the
current line shaded, Tab inserting 4 spaces, and Enter keeping the
indentation (one level deeper after a line ending in ":").

Coloring uses regular expressions, not a full Python parser, so an odd
case can be colored wrongly (such as a # inside a string). That's fine
for the short beginner programs this editor is used for.
"""

import re
import tkinter as tk
from tkinter import ttk

KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield",
]

BUILTINS = [
    "print", "input", "int", "float", "str", "bool", "list", "dict",
    "tuple", "set", "len", "range", "sum", "max", "min", "sorted",
    "enumerate", "zip", "abs", "round", "type", "open", "map", "filter",
]

# Each kind of word, the pattern that finds it, and its color.
# \b means a word boundary, so "in" is not found inside "print".
HIGHLIGHTS = [
    ("number", r"\b\d+(\.\d+)?\b", "#B15C00"),
    ("keyword", r"\b(" + "|".join(KEYWORDS) + r")\b", "#0057B7"),
    ("builtin", r"\b(" + "|".join(BUILTINS) + r")\b", "#7A3E9D"),
    ("string", r"(\"\"\".*?\"\"\"|'''.*?'''|\"[^\"\n]*\"|'[^'\n]*')", "#0B7A3E"),
    ("comment", r"#.*", "#8A8A8A"),
]


class CodeEditor(ttk.Frame):

    def __init__(self, parent, font):
        """Builds the line-number column, the text box and the scrollbar."""
        super().__init__(parent)

        self.line_numbers = tk.Text(self, width=4, padx=6, pady=4, takefocus=0, border=0,
                                    background="#EAEAEA", foreground="#8A8A8A",
                                    state="disabled", font=font, wrap="none")
        self.line_numbers.pack(side="left", fill="y")

        self.text = tk.Text(self, wrap="none", font=font, padx=6, pady=4, undo=True,
                            background="white", foreground="#1A1A1A",
                            insertbackground="black", border=0)
        self.text.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._on_scrollbar_moved)
        self.scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self._on_text_scrolled)

        self.text.tag_configure("current_line", background="#F3F3F3")
        for name, pattern, color in HIGHLIGHTS:
            self.text.tag_configure(name, foreground=color)

        self.text.bind("<KeyRelease>", self._on_change)
        self.text.bind("<ButtonRelease>", self._on_change)
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Return>", self._on_enter)
        self._redraw()

    def get_text(self) -> str:
        """Returns everything typed in the editor."""
        return self.text.get("1.0", "end-1c")

    def set_text(self, new_text: str):
        """Replaces everything in the editor with new_text."""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", new_text)
        self._redraw()

    def _on_scrollbar_moved(self, *args):
        """When the scrollbar is dragged, scrolls the text and line numbers together."""
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def _on_text_scrolled(self, first, last):
        """When the text scrolls by itself (e.g. while typing), moves the scrollbar and line numbers to match."""
        self.scrollbar.set(first, last)
        self.line_numbers.yview_moveto(first)

    def _on_tab(self, event):
        """
        Inserts 4 spaces. Returning "break" stops Tkinter's normal Tab
        behavior, which would move the focus to the next button.
        """
        self.text.insert("insert", "    ")
        return "break"

    def _on_enter(self, event):
        """
        Starts the new line with the same indentation as the current one,
        plus 4 more spaces if the current line ends with ":".
        """
        line = self.text.get("insert linestart", "insert")
        indent = re.match(r"[ \t]*", line).group(0)
        if line.rstrip().endswith(":"):
            indent += "    "
        self.text.insert("insert", "\n" + indent)
        return "break"

    def _on_change(self, event):
        """Redraws after every key press or click."""
        self._redraw()

    def _redraw(self):
        """Updates the line numbers, the colors and the shaded current line."""
        self._update_line_numbers()
        self._color_code()
        self.text.tag_remove("current_line", "1.0", "end")
        self.text.tag_add("current_line", "insert linestart", "insert lineend+1c")

    def _update_line_numbers(self):
        """Writes one number per line of code into the line-number column."""
        line_count = int(self.text.index("end-1c").split(".")[0])
        numbers = []
        for number in range(1, line_count + 1):
            numbers.append(str(number))

        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", "\n".join(numbers))
        self.line_numbers.config(state="disabled")

    def _color_code(self):
        """
        Colors every match of each pattern in HIGHLIGHTS. Strings and comments
        are raised to the top afterwards, so a keyword inside a string or a
        comment shows in the string's or comment's color.
        """
        code = self.get_text()
        for name, pattern, color in HIGHLIGHTS:
            self.text.tag_remove(name, "1.0", "end")
            for match in re.finditer(pattern, code):
                self.text.tag_add(name, f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        self.text.tag_raise("string")
        self.text.tag_raise("comment")
