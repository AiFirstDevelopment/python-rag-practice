import importlib.util
from pathlib import Path

import numpy as np

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Chunk = solution.Chunk
VOCAB = ["refund", "money", "ship", "deliver", "warranty", "repair"]


def embed(text):
    """A fake embedding: how many times each known word is in the text, plus a little so it is never all zeros."""
    return np.array([text.lower().count(word) + 0.01 for word in VOCAB])


CHUNKS = [
    Chunk("returns.txt", 1, 0, "A refund puts the money back on your card."),
    Chunk("shipping.txt", 1, 0, "We ship in two days and deliver by courier."),
    Chunk("warranty.txt", 1, 0, "The warranty covers one repair a year."),
]


def test_embed_chunks_is_one_row_per_chunk_in_order():
    vectors = solution.embed_chunks(CHUNKS, embed)
    assert vectors.shape == (3, len(VOCAB))
    for row, chunk in zip(vectors, CHUNKS):
        assert np.allclose(row, embed(chunk.text))


def test_nearest_is_best_first():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
    assert solution.nearest(vectors, np.array([1.0, 0.1]), 2) == [0, 2]


def test_nearest_is_cosine_similarity_not_the_dot_product():
    vectors = np.array([[10.0, 10.0], [1.0, 0.0]])       # the first row is long but points 45 degrees away
    assert solution.nearest(vectors, np.array([1.0, 0.0]), 2) == [1, 0]


def test_nearest_returns_plain_ints():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])
    result = solution.nearest(vectors, np.array([0.0, 1.0]), 2)
    assert all(type(i) is int for i in result)


def test_a_limit_past_the_end_gives_every_row():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert solution.nearest(vectors, np.array([1.0, 0.2]), 10) == [0, 1]


def test_vector_search_returns_the_nearest_chunks():
    vectors = solution.embed_chunks(CHUNKS, embed)
    found = solution.vector_search(CHUNKS, vectors, "Can I get my money back with a refund?", embed, 1)
    assert len(found) == 1
    assert found[0] is CHUNKS[0]
    found = solution.vector_search(CHUNKS, vectors, "When will you deliver?", embed, 3)
    assert found[0] is CHUNKS[1]
    assert len(found) == 3


def test_vector_search_with_no_chunks_gives_nothing_and_embeds_nothing():
    def never(text):
        raise AssertionError("embed was called")

    assert solution.vector_search([], np.zeros((0, 6)), "anything", never, 5) == []
