import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

RUN = {"passed": 18, "failed": 2, "note": "café", "cases": [{"id": "returns-01", "status": "pass"}]}
ROWS = [
    {"id": "returns-01", "question": "How long do I have to return an item?", "expected_behavior": "answer"},
    {"id": "absent-01", "question": "Do you sell café gift cards?", "expected_behavior": "fallback"},
]


def test_a_run_saved_is_the_run_loaded(tmp_path):
    path = tmp_path / "run.json"
    solution.save_run(path, RUN)
    assert solution.load_run(path) == RUN


def test_save_run_indents_and_keeps_non_ascii_characters(tmp_path):
    path = tmp_path / "run.json"
    solution.save_run(path, RUN)
    text = path.read_text(encoding="utf-8")
    assert json.loads(text) == RUN
    assert '\n  "passed": 18' in text
    assert "café" in text


def test_write_jsonl_puts_one_object_on_each_line(tmp_path):
    path = tmp_path / "golden.jsonl"
    solution.write_jsonl(path, ROWS)
    text = path.read_text(encoding="utf-8")
    assert text.endswith("\n") and "café" in text
    assert [json.loads(line) for line in text.splitlines()] == ROWS


def test_write_jsonl_replaces_the_file_and_no_rows_is_an_empty_file(tmp_path):
    path = tmp_path / "golden.jsonl"
    solution.write_jsonl(path, ROWS)
    solution.write_jsonl(path, ROWS[:1])
    assert solution.read_jsonl(path) == ROWS[:1]
    solution.write_jsonl(path, [])
    assert path.read_text(encoding="utf-8") == ""


def test_read_jsonl_skips_blank_lines(tmp_path):
    path = tmp_path / "golden.jsonl"
    path.write_text(json.dumps(ROWS[0]) + "\n\n   \n" + json.dumps(ROWS[1]) + "\n\n", encoding="utf-8")
    assert solution.read_jsonl(path) == ROWS


def test_read_jsonl_names_the_line_that_is_not_json(tmp_path):
    path = tmp_path / "golden.jsonl"
    path.write_text(json.dumps(ROWS[0]) + "\n\nnot json\n" + json.dumps(ROWS[1]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 3"):
        solution.read_jsonl(path)


def test_append_jsonl_adds_lines_and_creates_the_file(tmp_path):
    path = tmp_path / "results.jsonl"
    solution.append_jsonl(path, ROWS[0])
    solution.append_jsonl(path, ROWS[1])
    assert solution.read_jsonl(path) == ROWS
    assert len(path.read_text(encoding="utf-8").splitlines()) == 2


def test_append_jsonl_goes_after_what_write_jsonl_wrote(tmp_path):
    path = tmp_path / "results.jsonl"
    solution.write_jsonl(path, ROWS[:1])
    solution.append_jsonl(path, ROWS[1])
    assert solution.read_jsonl(path) == ROWS
