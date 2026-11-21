import json

import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def line(id="returns-01", **changes):
    case = {
        "id": id,
        "category": "answerable",
        "question": "How long do I have to return an item?",
        "expected_behavior": "answer",
        "required_facts": [{"fact": "30 days of delivery", "match": ["30 days", "thirty days"]}],
        "sources": [{"file": "returns.txt", "page": 1}],
    }
    case.update(changes)
    return json.dumps({k: v for k, v in case.items() if v is not None})


FALLBACK_LINE = line("absent-01", category="absent", expected_behavior="fallback", required_facts=[], sources=[])


def write(tmp_path, lines):
    path = tmp_path / "golden.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_each_line_becomes_a_case_in_file_order(tmp_path):
    cases = solution.load_cases(write(tmp_path, [line("returns-01"), line("returns-02"), FALLBACK_LINE]))
    assert [c.id for c in cases] == ["returns-01", "returns-02", "absent-01"]
    assert all(isinstance(c, solution.Case) for c in cases)


def test_facts_and_sources_are_models_too(tmp_path):
    case = solution.load_cases(write(tmp_path, [line()]))[0]
    assert isinstance(case.required_facts[0], solution.Fact)
    assert case.required_facts[0].fact == "30 days of delivery"
    assert case.required_facts[0].match == ["30 days", "thirty days"]
    assert isinstance(case.sources[0], solution.Source)
    assert (case.sources[0].file, case.sources[0].page) == ("returns.txt", 1)


def test_a_fallback_case_has_empty_lists(tmp_path):
    case = solution.load_cases(write(tmp_path, [FALLBACK_LINE]))[0]
    assert case.expected_behavior == "fallback"
    assert case.required_facts == [] and case.sources == []


def test_blank_lines_are_skipped(tmp_path):
    cases = solution.load_cases(write(tmp_path, ["", line("returns-01"), "   ", line("returns-02"), ""]))
    assert [c.id for c in cases] == ["returns-01", "returns-02"]


def test_a_line_that_is_not_json_is_reported_by_number(tmp_path):
    with pytest.raises(solution.GoldenSetError) as error:
        solution.load_cases(write(tmp_path, [line("returns-01"), "{not json", line("returns-02")]))
    assert error.value.lines == [2]


def test_a_value_that_is_not_allowed_is_a_bad_line(tmp_path):
    with pytest.raises(solution.GoldenSetError) as error:
        solution.load_cases(write(tmp_path, [line("returns-01", expected_behavior="answers")]))
    assert error.value.lines == [1]


def test_a_missing_field_is_a_bad_line(tmp_path):
    with pytest.raises(solution.GoldenSetError) as error:
        solution.load_cases(write(tmp_path, [line("returns-01"), line("returns-02", question=None)]))
    assert error.value.lines == [2]


def test_every_bad_line_is_reported_and_blank_lines_count(tmp_path):
    lines = [line("returns-01"), "oops", "", line("returns-02"), line("returns-03", category="easy")]
    with pytest.raises(solution.GoldenSetError) as error:
        solution.load_cases(write(tmp_path, lines))
    assert error.value.lines == [2, 5]


def test_an_id_used_twice_is_a_bad_line(tmp_path):
    with pytest.raises(solution.GoldenSetError) as error:
        solution.load_cases(write(tmp_path, [line("returns-01"), line("returns-02"), line("returns-01")]))
    assert error.value.lines == [3]
