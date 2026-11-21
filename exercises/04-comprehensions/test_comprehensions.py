import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)



def test_words_splits_on_punctuation_and_lowercases():
    assert solution.words("Refunds: 30 days, no receipt? Don't worry.") == [
        "refunds", "30", "days", "no", "receipt", "don't", "worry"]


def test_words_of_empty_text():
    assert solution.words("") == []


def test_words_handles_line_breaks_and_dashes():
    assert solution.words("store-credit\nonly") == ["store", "credit", "only"]


def test_keyword_hits_ignores_case_and_keeps_keys_as_given():
    assert solution.keyword_hits("Refund or refund? REFUND!", ["refund", "Receipt"]) == {"refund": 3, "Receipt": 0}


def test_keyword_hits_counts_whole_words_only():
    assert solution.keyword_hits("refunds refunded refund", ["refund"]) == {"refund": 1}
