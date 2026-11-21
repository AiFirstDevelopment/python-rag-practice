import importlib.util
from pathlib import Path
from typing import get_args, get_origin, get_type_hints

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def _plain(hint):
    """list[str] and typing.List[str] compare equal after this."""
    origin = get_origin(hint)
    return (origin, tuple(_plain(arg) for arg in get_args(hint))) if origin else hint


def _hints(function):
    return {name: _plain(hint) for name, hint in get_type_hints(function).items()}


def test_first_words_takes_the_first_n_words():
    assert solution.first_words("You can return any unused item within 30 days.", 3) == "You can return"


def test_first_words_defaults_to_five_and_joins_with_single_spaces():
    assert solution.first_words("one  two\nthree four five six") == "one two three four five"
    assert solution.first_words("only two") == "only two"


def test_first_words_is_hinted():
    assert _hints(solution.first_words) == {"text": str, "n": int, "return": str}


def test_page_lengths_counts_characters_per_page_from_page_one():
    assert solution.page_lengths(["Returns", "Shipping costs"]) == {1: 7, 2: 14}
    assert solution.page_lengths([]) == {}


def test_page_lengths_is_hinted():
    assert _hints(solution.page_lengths) == {"pages": _plain(list[str]), "return": _plain(dict[int, int])}


def test_longest_page_gives_number_and_text_earliest_on_a_tie():
    assert solution.longest_page(["Returns", "Shipping costs"]) == (2, "Shipping costs")
    assert solution.longest_page(["abc", "xyz", "no"]) == (1, "abc")


def test_longest_page_of_no_pages_raises():
    with pytest.raises(ValueError):
        solution.longest_page([])


def test_longest_page_is_hinted():
    assert _hints(solution.longest_page) == {"pages": _plain(list[str]), "return": _plain(tuple[int, str])}
