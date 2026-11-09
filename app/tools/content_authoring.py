"""
File: content_authoring.py
Author: Bior Madol Khom Bior
----------------------------
Shared code behind every write_<topic>_content.py script. Each of those
scripts only lists its problems; this file does the real work: it runs
each correct solution to get the expected outputs (they are never typed
by hand), checks that every "debug it" problem's broken code really
fails a test, and writes one JSON file per problem.
"""

import json
from pathlib import Path

from core.problem_loader import TestCase
from core.submission import run_and_grade_all, run_submission

CONTENT_ROOT = Path(__file__).parent.parent / "content"


def encode_tuples(value):
    """
    JSON has no tuple type, so this recursively replaces every tuple in
    value with {"__tuple__": [...]}. problem_loader.py turns these markers
    back into real tuples when it loads the problem.
    """
    if isinstance(value, tuple):
        items = []
        for item in value:
            items.append(encode_tuples(item))
        return {"__tuple__": items}
    if isinstance(value, list):
        items = []
        for item in value:
            items.append(encode_tuples(item))
        return items
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            result[key] = encode_tuples(item)
        return result
    return value


def compute_expected(solution: str, function_name: str, args_list: list) -> list:
    """
    Runs the correct solution once per argument list and returns what it
    printed each time. Raises an error if the solution crashes or times
    out, since that means the problem itself is wrong.
    """
    outputs = []
    for args in args_list:
        result = run_submission(solution, function_name, args=args)
        if not result.succeeded:
            raise RuntimeError(f"{function_name}{tuple(args)}: the solution failed:\n{result.stderr}")
        outputs.append(result.stdout.strip())
    return outputs


def starter_stub(solution: str, function_name: str) -> str:
    """
    Builds the starter code a student sees: the same function header as the
    solution, with its body replaced by a TODO. Any helper function written
    before it is kept, because the student is meant to be given it.
    """
    def_start = solution.index(f"def {function_name}(")
    given_code = solution[:def_start]
    parameters = solution[def_start:].split("(", 1)[1].split(")", 1)[0]
    return given_code + f"def {function_name}({parameters}):\n    # TODO: implement this\n    pass\n"


def build_tests(args_list: list, expected_outputs: list) -> list:
    """Pairs each argument list with its expected output, in JSON form."""
    tests = []
    for args, expected in zip(args_list, expected_outputs):
        tests.append({"args": encode_tuples(args), "expected_output": expected})
    return tests


def save_problem(folder: Path, problem: dict) -> None:
    """Writes one problem to <folder>/<id>.json."""
    path = folder / f"{problem['id']}.json"
    path.write_text(json.dumps(problem, indent=2), encoding="utf-8")


def write_topic(topic: str, folder_name: str, write_problems: list, debug_problems: list) -> int:
    """
    Deletes a topic's old problem files and writes the new ones. Returns how
    many files were written.

    write_problems holds (id, function_name, prompt, solution, args_list, hint)
    tuples. debug_problems holds (id, function_name, prompt, solution,
    buggy_code, args_list) tuples.
    """
    folder = CONTENT_ROOT / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    for old_file in folder.glob("*.json"):
        old_file.unlink()

    written = 0

    for problem_id, function_name, prompt, solution, args_list, hint in write_problems:
        expected_outputs = compute_expected(solution, function_name, args_list)
        save_problem(folder, {
            "id": problem_id,
            "topic": topic,
            "title": function_name,
            "prompt": prompt,
            "starter_code": starter_stub(solution, function_name),
            "function_name": function_name,
            "tests": build_tests(args_list, expected_outputs),
            "hint": hint,
            "solution": solution,
        })
        written += 1
        print(f"wrote {problem_id} ({function_name}) - {len(args_list)} test(s)")

    for problem_id, function_name, prompt, solution, buggy_code, args_list in debug_problems:
        expected_outputs = compute_expected(solution, function_name, args_list)

        # A debug problem only makes sense if its broken code fails at least one test.
        buggy_tests = []
        for args, expected in zip(args_list, expected_outputs):
            buggy_tests.append(TestCase(args=args, expected_output=expected))
        failed_count = 0
        for result in run_and_grade_all(buggy_code, function_name, buggy_tests):
            if not result.passed:
                failed_count += 1
        if failed_count == 0:
            raise RuntimeError(f"{problem_id}: the buggy starter code passes every test")

        save_problem(folder, {
            "id": problem_id,
            "topic": topic,
            "title": function_name,
            "prompt": prompt,
            "starter_code": buggy_code,
            "function_name": function_name,
            "tests": build_tests(args_list, expected_outputs),
            "hint": "",
            "solution": solution,
        })
        written += 1
        print(f"wrote {problem_id} ({function_name}, debug) - fails {failed_count}/{len(buggy_tests)} test(s)")

    return written
