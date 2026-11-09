"""
File: problem_loader.py
Author: Bior Madol Khom Bior
----------------------------
Reads the practice problems from the content folder. Each topic is a
subfolder such as content/05_loops/ (the number sets the order), with one
JSON file per problem. A problem file that is missing something raises
ProblemValidationError with the file's name, so mistakes are easy to find.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

# Every problem file must have these. "hint" is optional.
REQUIRED_FIELDS = {"id", "topic", "title", "prompt", "starter_code", "function_name", "tests", "solution"}


class ProblemValidationError(Exception):
    """Raised when a problem file is missing a field or is badly formed."""


@dataclass
class TestCase:
    __test__ = False  # tells pytest this is not a test class, despite its name

    expected_output: str
    args: list = field(default_factory=list)   # arguments passed to the function
    input: str = ""                             # text typed in for input() calls


@dataclass
class Problem:
    id: str
    topic: str
    title: str
    prompt: str
    starter_code: str
    function_name: str
    tests: list[TestCase]
    solution: str
    hint: str = ""


@dataclass
class Topic:
    name: str
    problems: list[Problem]


def decode_tuples(value):
    """
    JSON has no tuple type, so tuples are saved as {"__tuple__": [...]}
    (see tools/content_authoring.py). This recursively turns those markers
    back into real tuples, so a student sees (1, 2) and not [1, 2].
    """
    if isinstance(value, dict) and list(value.keys()) == ["__tuple__"]:
        items = []
        for item in value["__tuple__"]:
            items.append(decode_tuples(item))
        return tuple(items)
    if isinstance(value, list):
        items = []
        for item in value:
            items.append(decode_tuples(item))
        return items
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            result[key] = decode_tuples(item)
        return result
    return value


def read_test_case(data: dict, path: Path, index: int) -> TestCase:
    """Builds one TestCase from an entry of a problem's "tests" list."""
    if "expected_output" not in data:
        raise ProblemValidationError(f"{path}: tests[{index}] is missing 'expected_output'")
    args = []
    for arg in data.get("args", []):
        args.append(decode_tuples(arg))
    return TestCase(expected_output=data["expected_output"], args=args, input=data.get("input", ""))


def read_problem(path: Path) -> Problem:
    """Reads one problem JSON file and checks that nothing is missing."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ProblemValidationError(f"{path}: missing field(s): {sorted(missing)}")
    if not data["tests"]:
        raise ProblemValidationError(f"{path}: 'tests' must not be empty")

    tests = []
    for index, test_data in enumerate(data["tests"]):
        tests.append(read_test_case(test_data, path, index))

    return Problem(
        id=data["id"],
        topic=data["topic"],
        title=data["title"],
        prompt=data["prompt"],
        starter_code=data["starter_code"],
        function_name=data["function_name"],
        tests=tests,
        solution=data["solution"],
        hint=data.get("hint", ""),
    )


def topic_name_from_folder(folder_name: str) -> str:
    """Removes the ordering number from a folder name: "05_loops" -> "loops"."""
    parts = folder_name.split("_", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return folder_name


class ProblemLoader:
    """Loads every topic and problem from a content folder."""

    def __init__(self, content_dir):
        """Remembers where the content folder is. It must exist."""
        self.content_dir = Path(content_dir)
        if not self.content_dir.exists():
            raise FileNotFoundError(f"Content directory not found: {self.content_dir}")
        self._topics = {}

    def load_all(self) -> dict[str, Topic]:
        """
        Loads every topic folder, in folder-name order, and returns a dict
        from topic name to Topic. Folders with no problems are skipped.
        """
        self._topics = {}
        folders = []
        for path in self.content_dir.iterdir():
            if path.is_dir():
                folders.append(path)

        for folder in sorted(folders):
            problems = []
            for json_file in sorted(folder.glob("*.json")):
                problems.append(read_problem(json_file))
            if problems:
                name = topic_name_from_folder(folder.name)
                self._topics[name] = Topic(name, problems)
        return self._topics

    def get_topic(self, topic_name: str) -> Topic | None:
        """Returns the topic with this name, or None if there isn't one."""
        return self._topics.get(topic_name)

    def get_problem(self, topic_name: str, problem_id: str) -> Problem | None:
        """Returns the problem with this id in this topic, or None."""
        topic = self.get_topic(topic_name)
        if topic is None:
            return None
        for problem in topic.problems:
            if problem.id == problem_id:
                return problem
        return None
