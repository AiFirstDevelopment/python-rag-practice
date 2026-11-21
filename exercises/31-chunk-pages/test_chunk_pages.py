import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

LONG = "This is a sentence. " * 100          # 2,000 characters: three chunks


def test_chunk_is_a_dataclass_with_file_page_seq_text():
    chunk = solution.Chunk("a.pdf", 2, 5, "Some text.")
    assert (chunk.file, chunk.page, chunk.seq, chunk.text) == ("a.pdf", 2, 5, "Some text.")
    assert chunk == solution.Chunk(file="a.pdf", page=2, seq=5, text="Some text.")


def test_pages_count_from_one_and_seq_from_zero():
    chunks = solution.chunk_file("a.pdf", ["Page one.", "Page two."])
    assert [(c.file, c.page, c.seq, c.text) for c in chunks] == [
        ("a.pdf", 1, 0, "Page one."),
        ("a.pdf", 2, 1, "Page two."),
    ]


def test_a_long_page_gives_several_chunks_with_the_same_page():
    chunks = solution.chunk_file("a.pdf", [LONG])
    assert [c.page for c in chunks] == [1, 1, 1]
    assert all(len(c.text) <= 900 for c in chunks)


def test_seq_keeps_counting_across_pages():
    chunks = solution.chunk_file("a.pdf", [LONG, "Page two.", LONG])
    assert [c.seq for c in chunks] == [0, 1, 2, 3, 4, 5, 6]
    assert [c.page for c in chunks] == [1, 1, 1, 2, 3, 3, 3]


def test_an_empty_page_gives_no_chunk_but_keeps_its_page_number():
    chunks = solution.chunk_file("a.pdf", ["Page one.", "  \n ", "Page three."])
    assert [(c.page, c.seq) for c in chunks] == [(1, 0), (3, 1)]


def test_a_file_with_no_pages_gives_no_chunks():
    assert solution.chunk_file("a.pdf", []) == []
