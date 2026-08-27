"""Reads and validates problem definitions from a content directory.

Each topic is a subfolder (e.g. content/05_loops/) containing one JSON
file per problem. This module discovers topics from folder names
(stripped of their numeric prefix), loads and validates individual
problem files into the Problem and Topic dataclasses, and exposes a
simple in-memory structure that the GUI and core modules can query
through ProblemLoader. It does not know about Huffman compression - in
the packaged app, content/ is decompressed to a temp directory first,
and this loader just points at that temp directory, which keeps it
testable against plain JSON files without touching compression at all.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "topic",
    "title",
    "prompt",
    "starter_code",
    "expected_output",
    "function_name",
}
# test_input and hint are optional (some problems take no input)


class ProblemValidationError(Exception):
    """Raised when a problem JSON file is missing fields or malformed."""


@dataclass
class Problem:
    id: str
    topic: str
    title: str
    prompt: str
    starter_code: str
    expected_output: str
    function_name: str
    test_input: str = ""
    hint: str = ""

    @staticmethod
    def from_dict(data: dict, source_path: Path) -> "Problem":
        """Builds a Problem from a parsed JSON dict.

        Args:
            data: The parsed JSON object for a single problem.
            source_path: The file data came from, used in error messages.

        Returns:
            A validated Problem instance.

        Raises:
            ProblemValidationError: If data is missing any required field.
        """
        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            raise ProblemValidationError(
                f"{source_path}: missing required field(s): {sorted(missing)}"
            )
        return Problem(
            id=data["id"],
            topic=data["topic"],
            title=data["title"],
            prompt=data["prompt"],
            starter_code=data["starter_code"],
            expected_output=data["expected_output"],
            function_name=data["function_name"],
            test_input=data.get("test_input", ""),
            hint=data.get("hint", ""),
        )


@dataclass
class Topic:
    name: str
    problems: list[Problem] = field(default_factory=list)


class ProblemLoader:
    """Loads all topics/problems from a content directory."""

    def __init__(self, content_dir: str | Path):
        """Points the loader at a content directory.

        Args:
            content_dir: Path to the directory containing topic subfolders.

        Raises:
            FileNotFoundError: If content_dir does not exist.
        """
        self.content_dir = Path(content_dir)
        if not self.content_dir.exists():
            raise FileNotFoundError(f"Content directory not found: {self.content_dir}")
        self._topics: dict[str, Topic] = {}

    def load_all(self) -> dict[str, Topic]:
        """Loads every topic folder under content_dir.

        Returns:
            A dict mapping topic name to its Topic. Folders that contain
            no problem files are skipped.
        """
        self._topics = {}
        topic_folders = sorted(
            p for p in self.content_dir.iterdir() if p.is_dir()
        )
        for folder in topic_folders:
            topic_name = self._strip_numeric_prefix(folder.name)
            problems = self._load_topic_folder(folder)
            if problems:
                self._topics[topic_name] = Topic(name=topic_name, problems=problems)
        return self._topics

    def _load_topic_folder(self, folder: Path) -> list[Problem]:
        """Loads every problem JSON file in one topic folder.

        Args:
            folder: The topic folder to scan for problem JSON files.

        Returns:
            The problems found in folder, sorted by filename.
        """
        problems = []
        for json_file in sorted(folder.glob("*.json")):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            problem = Problem.from_dict(data, json_file)
            problems.append(problem)
        return problems

    @staticmethod
    def _strip_numeric_prefix(folder_name: str) -> str:
        """Removes a topic folder's numeric ordering prefix.

        Args:
            folder_name: A folder name such as "05_loops".

        Returns:
            The topic name with the prefix removed, e.g. "loops".
        """
        parts = folder_name.split("_", 1)
        if len(parts) == 2 and parts[0].isdigit():
            return parts[1]
        return folder_name

    def get_topic(self, topic_name: str) -> Topic | None:
        """Looks up a loaded topic by name.

        Args:
            topic_name: The topic to look up.

        Returns:
            The matching Topic, or None if no such topic was loaded.
        """
        return self._topics.get(topic_name)

    def get_problem(self, topic_name: str, problem_id: str) -> Problem | None:
        """Looks up a single problem by topic and id.

        Args:
            topic_name: The topic the problem belongs to.
            problem_id: The problem's unique id.

        Returns:
            The matching Problem, or None if not found.
        """
        topic = self.get_topic(topic_name)
        if not topic:
            return None
        for problem in topic.problems:
            if problem.id == problem_id:
                return problem
        return None

    @property
    def topic_names(self) -> list[str]:
        """Names of every topic currently loaded, in load order.

        Returns:
            A list of topic names.
        """
        return list(self._topics.keys())
