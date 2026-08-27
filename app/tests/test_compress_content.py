import json

from compress_content import compress_content, decompress_content


SAMPLE_PROBLEM = {
    "id": "loops_099",
    "topic": "loops",
    "title": "Test problem",
    "prompt": "Do something with loops and print the result clearly.",
    "starter_code": "for i in range(5):\n    print(i)\n",
    "expected_output": "0\n1\n2\n3\n4",
    "test_input": "",
    "hint": "Use range(5).",
}


def test_compress_then_decompress_round_trips_exactly(tmp_path):
    content_dir = tmp_path / "content"
    topic_dir = content_dir / "05_loops"
    topic_dir.mkdir(parents=True)

    problem_path = topic_dir / "loops_099.json"
    original_text = json.dumps(SAMPLE_PROBLEM, indent=2)
    problem_path.write_text(original_text, encoding="utf-8")

    archive_path = tmp_path / "content.huff"
    compress_content(content_dir, archive_path)

    output_dir = tmp_path / "decompressed"
    decompress_content(archive_path, output_dir)

    restored_text = (output_dir / "05_loops" / "loops_099.json").read_text(encoding="utf-8")
    assert restored_text == original_text


def test_round_trip_preserves_multiple_files_and_topics(tmp_path):
    content_dir = tmp_path / "content"
    for topic, pid in [("loops", "loops_001"), ("variables", "variables_001")]:
        topic_dir = content_dir / topic
        topic_dir.mkdir(parents=True)
        data = {**SAMPLE_PROBLEM, "id": pid, "topic": topic}
        (topic_dir / f"{pid}.json").write_text(json.dumps(data), encoding="utf-8")

    archive_path = tmp_path / "content.huff"
    compress_content(content_dir, archive_path)

    output_dir = tmp_path / "decompressed"
    decompress_content(archive_path, output_dir)

    assert (output_dir / "loops" / "loops_001.json").exists()
    assert (output_dir / "variables" / "variables_001.json").exists()


def test_round_trip_preserves_unicode_content(tmp_path):
    content_dir = tmp_path / "content"
    topic_dir = content_dir / "strings"
    topic_dir.mkdir(parents=True)
    data = {**SAMPLE_PROBLEM, "prompt": "café résumé naïve 日本語 🎉"}
    original_text = json.dumps(data, ensure_ascii=False)
    (topic_dir / "strings_001.json").write_text(original_text, encoding="utf-8")

    archive_path = tmp_path / "content.huff"
    compress_content(content_dir, archive_path)
    output_dir = tmp_path / "decompressed"
    decompress_content(archive_path, output_dir)

    restored_text = (output_dir / "strings" / "strings_001.json").read_text(encoding="utf-8")
    assert restored_text == original_text
