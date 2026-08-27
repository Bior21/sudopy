import json

import pytest

from core.problem_loader import ProblemLoader, ProblemValidationError


VALID_PROBLEM = {
    "id": "loops_099",
    "topic": "loops",
    "title": "Test problem",
    "prompt": "Do something.",
    "starter_code": "def test_problem():\n    print('hi')\n",
    "expected_output": "hi",
    "function_name": "test_problem",
}


def write_problem(folder, filename, data):
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / filename, "w") as f:
        json.dump(data, f)


def test_loads_single_topic_single_problem(tmp_path):
    write_problem(tmp_path / "05_loops", "p1.json", VALID_PROBLEM)

    loader = ProblemLoader(tmp_path)
    topics = loader.load_all()

    assert "loops" in topics
    assert len(topics["loops"].problems) == 1
    assert topics["loops"].problems[0].id == "loops_099"


def test_numeric_prefix_is_stripped_from_topic_name(tmp_path):
    write_problem(tmp_path / "01_variables", "p1.json", {**VALID_PROBLEM, "topic": "variables"})

    loader = ProblemLoader(tmp_path)
    topics = loader.load_all()

    assert "variables" in topics
    assert "01_variables" not in topics


def test_multiple_problems_in_one_topic(tmp_path):
    folder = tmp_path / "05_loops"
    write_problem(folder, "p1.json", {**VALID_PROBLEM, "id": "loops_001"})
    write_problem(folder, "p2.json", {**VALID_PROBLEM, "id": "loops_002"})

    loader = ProblemLoader(tmp_path)
    topics = loader.load_all()

    assert len(topics["loops"].problems) == 2


def test_missing_required_field_raises(tmp_path):
    bad_problem = {k: v for k, v in VALID_PROBLEM.items() if k != "expected_output"}
    write_problem(tmp_path / "05_loops", "bad.json", bad_problem)

    loader = ProblemLoader(tmp_path)
    with pytest.raises(ProblemValidationError):
        loader.load_all()


def test_optional_fields_default_when_missing(tmp_path):
    minimal = {k: v for k, v in VALID_PROBLEM.items()}
    # test_input and hint intentionally omitted
    write_problem(tmp_path / "05_loops", "p1.json", minimal)

    loader = ProblemLoader(tmp_path)
    topics = loader.load_all()
    problem = topics["loops"].problems[0]

    assert problem.test_input == ""
    assert problem.hint == ""


def test_get_problem_by_topic_and_id(tmp_path):
    write_problem(tmp_path / "05_loops", "p1.json", VALID_PROBLEM)

    loader = ProblemLoader(tmp_path)
    loader.load_all()

    problem = loader.get_problem("loops", "loops_099")
    assert problem is not None
    assert problem.title == "Test problem"

    assert loader.get_problem("loops", "does_not_exist") is None
    assert loader.get_problem("no_such_topic", "loops_099") is None


def test_nonexistent_content_dir_raises():
    with pytest.raises(FileNotFoundError):
        ProblemLoader("/path/that/does/not/exist")


def test_empty_topic_folder_is_skipped(tmp_path):
    (tmp_path / "05_loops").mkdir(parents=True)  # no json files inside
    write_problem(tmp_path / "01_variables", "p1.json", {**VALID_PROBLEM, "topic": "variables"})

    loader = ProblemLoader(tmp_path)
    topics = loader.load_all()

    assert "loops" not in topics
    assert "variables" in topics
