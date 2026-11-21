import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Passage, Source, Case = solution.Passage, solution.Source, solution.Case


def case(*sources):
    return Case(
        id="c", category="answerable" if sources else "absent", question="?",
        expected_behavior="answer" if sources else "fallback", required_facts=[],
        sources=[Source(file=f, page=p) for f, p in sources],
    )


PASSAGES = [Passage("shipping.pdf", 2, 4, "..."), Passage("returns.txt", 1, 1, "...")]


def test_found_on_a_one_page_passage():
    assert solution.source_found(Source(file="returns.txt", page=1), PASSAGES) is True


def test_found_anywhere_in_a_passage_that_spans_pages():
    for page in (2, 3, 4):
        assert solution.source_found(Source(file="shipping.pdf", page=page), PASSAGES) is True


def test_not_found_outside_the_pages():
    assert solution.source_found(Source(file="shipping.pdf", page=1), PASSAGES) is False
    assert solution.source_found(Source(file="shipping.pdf", page=5), PASSAGES) is False


def test_the_same_page_in_another_file_does_not_count():
    assert solution.source_found(Source(file="warranty.txt", page=1), PASSAGES) is False


def test_recall_is_the_fraction_of_sources_found():
    assert solution.recall(case(("returns.txt", 1), ("shipping.pdf", 3)), PASSAGES) == 1.0
    assert solution.recall(case(("returns.txt", 1), ("warranty.txt", 1)), PASSAGES) == 0.5
    assert solution.recall(case(("warranty.txt", 1)), PASSAGES) == 0.0


def test_recall_with_no_passages_is_zero():
    assert solution.recall(case(("returns.txt", 1)), []) == 0.0


def test_recall_of_a_case_without_sources_is_none():
    assert solution.recall(case(), PASSAGES) is None


def test_mean_recall_leaves_out_the_nones():
    assert solution.mean_recall([1.0, 0.5, None]) == pytest.approx(0.75)


def test_mean_recall_of_nothing_to_average_is_zero():
    assert solution.mean_recall([]) == 0.0
    assert solution.mean_recall([None, None]) == 0.0
