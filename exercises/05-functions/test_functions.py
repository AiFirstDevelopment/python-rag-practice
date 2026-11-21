import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)



def test_defaults():
    assert solution.make_chunk("Returns within 30 days.", "returns.pdf") == {
        "text": "Returns within 30 days.", "source": "returns.pdf", "page": 1, "tags": []}


def test_keyword_arguments():
    chunk = solution.make_chunk("Sale items are final.", "returns.pdf", page=2, tags=["sale"])
    assert chunk["page"] == 2 and chunk["tags"] == ["sale"]


def test_chunks_without_tags_do_not_share_a_list():
    a = solution.make_chunk("one", "a.pdf")
    b = solution.make_chunk("two", "a.pdf")
    solution.add_tag(a, "x")
    assert b["tags"] == []


def test_given_tags_are_copied():
    tags = ["sale"]
    chunk = solution.make_chunk("x", "a.pdf", tags=tags)
    solution.add_tag(chunk, "final")
    assert tags == ["sale"]


def test_add_tag_skips_duplicates_and_returns_the_chunk():
    chunk = solution.make_chunk("x", "a.pdf", tags=["sale"])
    assert solution.add_tag(chunk, "sale") is chunk
    assert chunk["tags"] == ["sale"]
