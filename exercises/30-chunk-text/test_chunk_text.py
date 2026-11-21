import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def test_a_short_page_is_one_stripped_piece():
    assert solution.chunk_page("  One sentence.  ") == ["One sentence."]


def test_an_empty_or_blank_page_gives_no_pieces():
    assert solution.chunk_page("") == []
    assert solution.chunk_page(" \n\t ") == []


def test_a_page_of_exactly_900_characters_is_one_piece():
    assert solution.chunk_page("x" * 900) == ["x" * 900]


def test_pieces_fit_and_end_at_a_sentence():
    text = "This is a sentence. " * 100
    pieces = solution.chunk_page(text)
    assert len(pieces) > 1
    assert all(len(p) <= 900 for p in pieces)
    assert all(p.endswith(".") for p in pieces)
    assert " ".join(pieces) == text.strip()


def test_a_line_break_after_a_period_ends_a_sentence():
    pieces = solution.chunk_page(("word " * 100 + "end.\n") * 3)
    assert pieces[0].endswith("end.")


def test_a_sentence_end_past_halfway_wins_over_a_later_space():
    pieces = solution.chunk_page("a" * 500 + ". " + "b " * 300)
    assert pieces[0] == "a" * 500 + "."


def test_a_sentence_end_before_halfway_is_ignored_and_the_cut_is_at_a_space():
    pieces = solution.chunk_page("Short. " + "word " * 300)
    assert len(pieces[0]) > 450
    assert len(pieces[0]) <= 900
    assert pieces[0].endswith("word")


def test_no_space_at_all_cuts_at_the_limit():
    assert [len(p) for p in solution.chunk_page("x" * 2000)] == [900, 900, 200]
