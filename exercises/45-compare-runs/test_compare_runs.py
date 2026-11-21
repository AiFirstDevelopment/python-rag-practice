import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Comparison = solution.Comparison


def test_gained_and_lost_are_the_flips_in_alphabetical_order():
    before = {"d": "pass", "c": "fail", "b": "fail", "a": "pass", "e": "pass"}
    after = {"d": "fail", "c": "pass", "b": "pass", "a": "fail", "e": "pass"}
    assert solution.compare(before, after) == Comparison(gained=["b", "c"], lost=["a", "d"], net=0)


def test_cases_that_did_not_change_are_in_neither_list():
    run = {"a": "pass", "b": "fail", "c": "review"}
    assert solution.compare(run, dict(run)) == Comparison(gained=[], lost=[], net=0)


def test_review_counts_as_not_passing():
    before = {"a": "review", "b": "pass", "c": "fail", "d": "review"}
    after = {"a": "pass", "b": "review", "c": "review", "d": "fail"}
    assert solution.compare(before, after) == Comparison(gained=["a"], lost=["b"], net=0)


def test_an_id_in_only_one_run_is_ignored():
    before = {"a": "fail", "old": "pass"}
    after = {"a": "pass", "new": "pass"}
    assert solution.compare(before, after) == Comparison(gained=["a"], lost=[], net=1)


def test_net_is_gained_minus_lost():
    before = {"a": "fail", "b": "fail", "c": "fail", "d": "pass"}
    after = {"a": "pass", "b": "pass", "c": "pass", "d": "fail"}
    assert solution.compare(before, after).net == 2


def test_a_net_at_the_threshold_is_a_gain_or_a_drop():
    assert solution.verdict(Comparison(gained=["a", "b"], lost=[], net=2)) == "gain"
    assert solution.verdict(Comparison(gained=[], lost=["a", "b"], net=-2)) == "drop"


def test_a_net_under_the_threshold_is_noise():
    assert solution.verdict(Comparison(gained=["a"], lost=[], net=1)) == "noise"
    assert solution.verdict(Comparison(gained=[], lost=["a"], net=-1)) == "noise"
    assert solution.verdict(Comparison(gained=["a", "b", "c"], lost=["d", "e", "f"], net=0)) == "noise"


def test_the_threshold_can_be_changed():
    assert solution.verdict(Comparison(gained=[], lost=["a"], net=-1), threshold=1) == "drop"
    assert solution.verdict(Comparison(gained=["a", "b"], lost=[], net=2), threshold=3) == "noise"
