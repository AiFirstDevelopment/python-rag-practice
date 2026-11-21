import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

STOP = {"the", "is", "a"}


def test_most_frequent_first_ties_alphabetical():
    text = "The refund is a refund. The receipt is the proof."
    assert solution.top_words(text, 2, STOP) == [("refund", 2), ("proof", 1)]


def test_all_when_n_is_large():
    assert solution.top_words("b a b", 10, set()) == [("b", 2), ("a", 1)]


def test_stopwords_in_any_case():
    assert solution.top_words("The THE the cat", 5, {"The"}) == [("cat", 1)]


def test_n_zero():
    assert solution.top_words("a b c", 0, set()) == []


def test_empty_text():
    assert solution.top_words("", 3, STOP) == []
