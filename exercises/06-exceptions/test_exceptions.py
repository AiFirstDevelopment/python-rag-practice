import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)



def test_parses_with_spaces():
    assert solution.parse_score(" 0.8 ") == 0.8


def test_ends_of_the_range_are_allowed():
    assert solution.parse_score("0") == 0.0
    assert solution.parse_score("1") == 1.0


def test_not_a_number_raises_with_the_text_in_the_message():
    with pytest.raises(ValueError, match="high"):
        solution.parse_score("high")


def test_out_of_range_raises():
    with pytest.raises(ValueError, match="1.5"):
        solution.parse_score("1.5")


def test_negative_raises():
    with pytest.raises(ValueError):
        solution.parse_score("-0.1")


def test_parse_all_keeps_good_scores_and_positions_of_bad_ones():
    assert solution.parse_all(["0.9", "high", "1.5", "0"]) == ([0.9, 0.0], [1, 2])


def test_parse_all_of_nothing():
    assert solution.parse_all([]) == ([], [])
