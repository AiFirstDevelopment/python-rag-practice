import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def test_clean_collapses_whitespace_runs():
    assert solution.clean("Returns are\n accepted   within\t30 days.") == "Returns are accepted within 30 days."


def test_clean_strips_the_ends():
    assert solution.clean("  \n Hello world \t ") == "Hello world"


def test_clean_of_only_whitespace_is_empty():
    assert solution.clean(" \n\t ") == ""


def test_preview_cuts_and_marks_long_text():
    assert solution.preview("Returns are accepted", 7) == "Returns..."


def test_preview_leaves_short_text_alone():
    assert solution.preview("Short", 10) == "Short"


def test_preview_of_exactly_n_characters_has_no_marker():
    assert solution.preview("Exact", 5) == "Exact"
