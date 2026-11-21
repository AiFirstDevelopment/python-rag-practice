import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Chunk, Passage = solution.Chunk, solution.Passage


def parts(n=5, file="f.txt"):
    return [Chunk(file, 1, i, f"part {i}.") for i in range(n)]


def test_a_chunk_gets_the_chunk_before_and_after_in_one_passage():
    chunks = parts()
    assert solution.widen([chunks[2]], chunks) == [Passage("f.txt", 1, 1, "part 1.\npart 2.\npart 3.")]


def test_the_first_and_last_chunk_of_a_file_have_one_neighbour():
    chunks = parts()
    assert [p.text for p in solution.widen([chunks[0]], chunks)] == ["part 0.\npart 1."]
    assert [p.text for p in solution.widen([chunks[4]], chunks)] == ["part 3.\npart 4."]


def test_given_chunks_side_by_side_become_one_passage():
    chunks = parts()
    assert [p.text for p in solution.widen([chunks[1], chunks[2]], chunks)] == ["part 0.\npart 1.\npart 2.\npart 3."]
    assert [p.text for p in solution.widen([chunks[2], chunks[1]], chunks)] == ["part 0.\npart 1.\npart 2.\npart 3."]


def test_neighbours_never_cross_files():
    chunks = [Chunk("a.txt", 1, 0, "a0."), Chunk("b.txt", 1, 1, "b1."), Chunk("b.txt", 1, 2, "b2.")]
    assert solution.widen([chunks[1]], chunks) == [Passage("b.txt", 1, 1, "b1.\nb2.")]


def test_a_passage_covers_the_pages_of_its_first_and_last_chunk():
    chunks = [Chunk("f.pdf", page, seq, f"part {seq}.") for seq, page in enumerate([1, 1, 2, 3, 3])]
    [passage] = solution.widen([chunks[2]], chunks)
    assert (passage.first_page, passage.last_page) == (1, 3)
    [passage] = solution.widen([chunks[4]], chunks)
    assert (passage.first_page, passage.last_page) == (3, 3)


def test_passages_come_in_the_order_of_the_given_chunks():
    chunks = parts(9)
    passages = solution.widen([chunks[7], chunks[1]], chunks)
    assert [p.text for p in passages] == ["part 6.\npart 7.\npart 8.", "part 0.\npart 1.\npart 2."]


def test_the_budget_stops_widening_and_the_best_chunk_is_served_first():
    chunks = [Chunk("f.txt", 1, i, "x" * 6000) for i in range(5)]
    [first, second] = solution.widen([chunks[1], chunks[3]], chunks)
    # chunk 1 takes chunk 0 (6,000 characters); a second neighbour would pass 10,800, so chunks 2 and 4 stay out
    assert (first.text.count("x"), second.text.count("x")) == (12000, 6000)


def test_a_neighbour_too_big_is_skipped_and_a_smaller_one_still_fits():
    chunks = [Chunk("f.txt", 1, 0, "x" * 50), Chunk("f.txt", 1, 1, "given."), Chunk("f.txt", 1, 2, "small.")]
    assert [p.text for p in solution.widen([chunks[1]], chunks, budget=10)] == ["given.\nsmall."]
    assert [p.text for p in solution.widen([chunks[1]], chunks, budget=0)] == ["given."]
    assert solution.widen([], chunks) == []
