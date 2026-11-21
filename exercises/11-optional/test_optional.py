import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

CHUNKS = [
    {"file": "returns.txt", "page": 1, "text": "Returns within 30 days."},
    {"file": "shipping.pdf", "page": 1, "text": "Standard shipping takes 5 days."},
    {"file": "shipping.pdf", "page": 2, "text": "Express shipping costs $19.95."},
    {"file": "shipping.pdf", "page": 2, "text": "Express orders ship the same day."},
]


def test_find_chunk_returns_the_first_match():
    assert solution.find_chunk(CHUNKS, "shipping.pdf", 2) is CHUNKS[2]


def test_find_chunk_returns_none_when_nothing_matches():
    assert solution.find_chunk(CHUNKS, "returns.txt", 2) is None
    assert solution.find_chunk([], "returns.txt", 1) is None


def test_page_label_for_one_page_and_for_a_range():
    assert solution.page_label(3) == "p.3"
    assert solution.page_label(3, None) == "p.3"
    assert solution.page_label(3, 3) == "p.3"
    assert solution.page_label(3, 5) == "pp.3-5"


def test_to_pages_from_a_number_or_a_string():
    assert solution.to_pages(4) == [4]
    assert solution.to_pages("4") == [4]
    assert solution.to_pages(" 4 ") == [4]


def test_to_pages_from_a_range():
    assert solution.to_pages("3-5") == [3, 4, 5]
    assert solution.to_pages(" 3 - 5 ") == [3, 4, 5]


def test_to_pages_copies_a_list():
    pages = [2, 7]
    result = solution.to_pages(pages)
    assert result == [2, 7] and result is not pages


def test_to_pages_refuses_other_text():
    with pytest.raises(ValueError):
        solution.to_pages("three")
    with pytest.raises(ValueError):
        solution.to_pages("1-2-3")


def test_retrieved_label_tells_none_from_false():
    assert solution.retrieved_label(True) == "found"
    assert solution.retrieved_label(False) == "missed"
    assert solution.retrieved_label(None) == "no source"
