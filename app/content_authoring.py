"""Shared machinery for the per-topic content-authoring scripts.

Each topic gets its own one-time script (write_loops_content.py,
write_variables_content.py, etc.) that supplies problem data - prompts,
solutions, test arguments - and calls write_topic() here to do the
actual work: compute every expected_output by really executing the
solution (never hand-typed), confirm every debug problem's buggy
starter_code genuinely fails at least one test, and write the JSON files.

Keeping this logic in one place means all topics get the same
correctness guarantees for free, rather than each script re-implementing
(and risking drift in) the same checks.
"""

import json
from pathlib import Path

from core.submission import run_and_grade_all
from core.problem_loader import TestCase

CONTENT_ROOT = Path(__file__).parent / "content"


def _encode_tuples(value):
    """Recursively turns real tuples into {"__tuple__": [...]} markers.

    JSON has no tuple type, so a real Python tuple in a script's args_list
    (e.g. write_tuples_content.py passing (3, 4) as an argument) would
    otherwise silently flatten to a JSON array and load back as a list -
    see problem_loader.py's matching _decode_tuples for why that matters.
    """
    if isinstance(value, tuple):
        return {"__tuple__": [_encode_tuples(v) for v in value]}
    if isinstance(value, list):
        return [_encode_tuples(v) for v in value]
    if isinstance(value, dict):
        return {k: _encode_tuples(v) for k, v in value.items()}
    return value


def compute_expected(solution_code: str, function_name: str, args_list: list) -> list:
    """Runs a correct solution for real to get each test's expected_output.

    Args:
        solution_code: A correct, function-based solution.
        function_name: The function's name.
        args_list: One argument list per test case.

    Returns:
        One expected_output string per entry in args_list.

    Raises:
        RuntimeError: If the solution crashes or times out on any input -
            that means the input choice or the "correct" solution is
            wrong, not that content should ship with a bad expected value.
    """
    tests = [TestCase(args=args, expected_output="") for args in args_list]
    results = run_and_grade_all(solution_code, function_name, tests)
    outputs = []
    for args, result in zip(args_list, results):
        if result.reason.startswith("Your code crashed") or result.reason.startswith("Your code took too long"):
            raise RuntimeError(f"{function_name}{tuple(args)}: reference solution failed: {result.reason}")
        outputs.append(result.actual_output.strip())
    return outputs


def starter_stub(solution: str, function_name: str) -> str:
    """Builds starter_code from a correct solution by stubbing out one function.

    Finds function_name's own `def` line within solution and replaces
    just that function's body with a TODO. Anything before it - a
    decomposition problem's already-working helper function, e.g. - is
    kept verbatim, since that's meant to be given to the student, not
    written by them.

    Args:
        solution: A correct, function-based solution. May define a
            helper function before function_name.
        function_name: The name of the function to stub out.

    Returns:
        A starter_code stub.
    """
    marker = f"def {function_name}("
    marker_index = solution.index(marker)
    preamble = solution[:marker_index]
    params_line = solution[marker_index:].split("(", 1)[1].split(")", 1)[0]
    return preamble + f"def {function_name}({params_line}):\n    # TODO: implement this\n    pass\n"


def write_topic(topic: str, folder_name: str, write_problems: list, debug_problems: list) -> int:
    """Writes a topic's full set of problem JSON files, clearing old ones first.

    Args:
        topic: The topic name stored in each problem's "topic" field
            (e.g. "variables").
        folder_name: The content subfolder to write into (e.g.
            "01_variables"), relative to content/.
        write_problems: A list of (id, function_name, prompt, solution,
            args_list, hint) tuples - the write-from-scratch problems.
        debug_problems: A list of (id, function_name, prompt, solution,
            buggy_starter_code, args_list) tuples - the debug-it problems.

    Returns:
        How many problem files were written.

    Raises:
        RuntimeError: If a debug problem's buggy_starter_code doesn't
            actually fail any test - it wouldn't be a real bug to find.
    """
    content_dir = CONTENT_ROOT / folder_name
    content_dir.mkdir(parents=True, exist_ok=True)
    for old_file in content_dir.glob("*.json"):
        old_file.unlink()

    written = 0

    for problem_id, function_name, prompt, solution, args_list, hint in write_problems:
        expected_outputs = compute_expected(solution, function_name, args_list)
        data = {
            "id": problem_id,
            "topic": topic,
            "title": function_name,
            "prompt": prompt,
            "starter_code": starter_stub(solution, function_name),
            "function_name": function_name,
            "tests": [
                {"args": _encode_tuples(args), "expected_output": expected}
                for args, expected in zip(args_list, expected_outputs)
            ],
            "hint": hint,
        }
        (content_dir / f"{problem_id}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        written += 1
        print(f"wrote {problem_id} ({function_name}) - {len(args_list)} test(s)")

    for problem_id, function_name, prompt, solution, buggy_code, args_list in debug_problems:
        expected_outputs = compute_expected(solution, function_name, args_list)

        buggy_tests = [
            TestCase(args=args, expected_output=expected)
            for args, expected in zip(args_list, expected_outputs)
        ]
        buggy_results = run_and_grade_all(buggy_code, function_name, buggy_tests)
        if all(r.passed for r in buggy_results):
            raise RuntimeError(f"{problem_id}: buggy starter_code passes every test - not actually buggy!")

        data = {
            "id": problem_id,
            "topic": topic,
            "title": function_name,
            "prompt": prompt,
            "starter_code": buggy_code,
            "function_name": function_name,
            "tests": [
                {"args": _encode_tuples(args), "expected_output": expected}
                for args, expected in zip(args_list, expected_outputs)
            ],
            "hint": "",
        }
        (content_dir / f"{problem_id}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        written += 1
        print(f"wrote {problem_id} ({function_name}, debug) - confirmed buggy on "
              f"{sum(1 for r in buggy_results if not r.passed)}/{len(buggy_results)} test(s)")

    return written
