import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Chunk = solution.Chunk


def chunk(seq, text):
    return Chunk("f.txt", 1, seq, text)


def test_ranks_the_matches_and_drops_the_rest():
    chunks = [chunk(0, "shipping is free"), chunk(1, "refund refund policy"), chunk(2, "refund window policy")]
    assert solution.bm25(chunks, "refund", 5) == [chunks[1], chunks[2]]


def test_returns_the_same_chunk_objects():
    chunks = [chunk(0, "refund policy"), chunk(1, "shipping rates")]
    [found] = solution.bm25(chunks, "shipping", 5)
    assert found is chunks[1]


def test_keeps_at_most_limit():
    chunks = [chunk(0, "refund"), chunk(1, "refund refund window"), chunk(2, "refund window policy text")]
    assert len(solution.bm25(chunks, "refund", 2)) == 2
    assert len(solution.bm25(chunks, "refund", 10)) == 3


def test_no_chunks_or_no_shared_word_gives_an_empty_list():
    assert solution.bm25([], "refund", 5) == []
    assert solution.bm25([chunk(0, "shipping is free")], "refund", 5) == []
    assert solution.bm25([chunk(0, "shipping is free")], "is the", 5) == []


def test_the_question_goes_through_words_too():
    chunks = [chunk(0, "the return window"), chunk(1, "shipping rates")]
    assert solution.bm25(chunks, "What are the RETURNS?", 5) == [chunks[0]]


def test_a_rare_word_outweighs_a_common_one():
    # "refund" is in four of the five chunks, "warranty" in one
    chunks = [chunk(0, "refund refund note"), chunk(1, "warranty note text"), chunk(2, "refund form here"),
              chunk(3, "refund desk hours"), chunk(4, "refund by mail")]
    assert solution.bm25(chunks, "refund warranty", 5)[0] is chunks[1]


def test_of_two_chunks_with_the_word_once_the_shorter_ranks_first():
    chunks = [chunk(0, "refund paid back within ten working days by bank transfer"), chunk(1, "refund paid")]
    assert solution.bm25(chunks, "refund", 5) == [chunks[1], chunks[0]]


def test_a_word_twice_in_the_question_counts_once():
    chunks = [chunk(0, "refund refund note"), chunk(1, "warranty note text"), chunk(2, "refund form here"),
              chunk(3, "refund desk hours"), chunk(4, "refund by mail")]
    assert solution.bm25(chunks, "refund refund refund refund warranty", 5)[0] is chunks[1]
