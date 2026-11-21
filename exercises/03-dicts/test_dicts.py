import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

RUNS = [
    {"category": "absent", "result": "pass"},
    {"category": "answerable", "result": "fail"},
    {"category": "answerable", "result": "pass"},
]


def test_count_by_category():
    assert solution.count_by(RUNS, "category") == {"absent": 1, "answerable": 2}


def test_count_by_result():
    assert solution.count_by(RUNS, "result") == {"pass": 2, "fail": 1}


def test_missing_key_counts_under_none():
    assert solution.count_by([{"a": 1}, {"b": 2}], "a") == {1: 1, None: 1}


def test_count_by_empty_list():
    assert solution.count_by([], "category") == {}


def test_pass_rate_rounds_to_two_places():
    assert solution.pass_rate(RUNS) == 0.67


def test_pass_rate_of_nothing_is_zero():
    assert solution.pass_rate([]) == 0.0


def test_pass_rate_ignores_review():
    assert solution.pass_rate([{"result": "pass"}, {"result": "review"}]) == 0.5
