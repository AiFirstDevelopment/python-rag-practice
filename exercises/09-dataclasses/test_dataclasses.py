import dataclasses
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution_09", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = solution      # dataclasses and pydantic look a class's module up by name
_spec.loader.exec_module(solution)

TEXT = "You can return any unused item within 30 days."


def test_chunk_is_a_dataclass_with_its_four_fields_in_order():
    assert dataclasses.is_dataclass(solution.Chunk)
    assert [f.name for f in dataclasses.fields(solution.Chunk)] == ["file", "page", "seq", "text"]
    chunk = solution.Chunk("returns.txt", 1, 0, TEXT)
    assert (chunk.file, chunk.page, chunk.seq, chunk.text) == ("returns.txt", 1, 0, TEXT)


def test_chunks_with_the_same_fields_are_equal():
    assert solution.Chunk("returns.txt", 1, 0, TEXT) == solution.Chunk(file="returns.txt", page=1, seq=0, text=TEXT)
    assert solution.Chunk("returns.txt", 1, 0, TEXT) != solution.Chunk("returns.txt", 2, 0, TEXT)


def test_preview_shows_file_page_and_first_words():
    chunk = solution.Chunk("returns.txt", 1, 0, TEXT)
    assert chunk.preview() == "returns.txt p.1: You can return any unused"
    assert chunk.preview(2) == "returns.txt p.1: You can"


def test_result_defaults():
    result = solution.Result("returns-01", True)
    assert dataclasses.is_dataclass(solution.Result)
    assert (result.id, result.retrieved, result.status, result.missing) == ("returns-01", True, "not run", [])


def test_result_fields_can_be_given():
    result = solution.Result("absent-01", None, status="fail", missing=["30 days"])
    assert result.retrieved is None and result.status == "fail" and result.missing == ["30 days"]


def test_results_do_not_share_a_missing_list():
    a = solution.Result("a", True)
    b = solution.Result("b", False)
    a.missing.append("store credit")
    assert b.missing == []


def test_chunks_of_numbers_pages_from_one_and_chunks_from_zero():
    assert solution.chunks_of("a.pdf", ["First.", "Second."]) == [
        solution.Chunk("a.pdf", 1, 0, "First."), solution.Chunk("a.pdf", 2, 1, "Second.")]
    assert solution.chunks_of("a.pdf", []) == []


def test_chunks_of_skips_empty_pages_but_keeps_page_numbers():
    assert solution.chunks_of("a.pdf", ["First.", "  \n", "", "Fourth."]) == [
        solution.Chunk("a.pdf", 1, 0, "First."), solution.Chunk("a.pdf", 4, 1, "Fourth.")]
