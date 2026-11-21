import hashlib
import re

import numpy as np
import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


TEXTS = [
    "returns are accepted within 30 days",
    "shipping takes five days",
    "gift cards never expire",
    "sale items are final",
]


def embed(text, size=64):
    """The tests' own stand-in for an embedding model: each word counted into one of 64 slots."""
    vector = np.zeros(size)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % size] += 1.0
    return vector


def cosine(a, b):
    lengths = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(a @ b) / lengths if lengths else 0.0


def test_normalize_rows_makes_every_row_length_one():
    unit = solution.normalize_rows(np.array([[3.0, 4.0], [0.0, 2.0]]))
    assert np.allclose(unit, [[0.6, 0.8], [0.0, 1.0]])


def test_a_row_of_zeros_stays_zeros():
    unit = solution.normalize_rows(np.array([[3.0, 4.0], [0.0, 0.0]]))
    assert not np.isnan(unit).any()
    assert np.allclose(unit[1], [0.0, 0.0])


def test_normalize_rows_does_not_change_the_matrix_given():
    matrix = np.array([[3.0, 4.0], [0.0, 2.0]])
    solution.normalize_rows(matrix)
    assert np.allclose(matrix, [[3.0, 4.0], [0.0, 2.0]])


def test_build_index_has_one_normalized_row_per_text_in_order():
    index = solution.build_index(TEXTS, embed)
    assert index.shape == (4, 64)
    assert np.allclose(np.linalg.norm(index, axis=1), 1.0)
    assert cosine(index[1], embed(TEXTS[1])) == pytest.approx(1.0)


def test_search_finds_the_text_that_shares_the_questions_words():
    index = solution.build_index(TEXTS, embed)
    result = solution.search(index, embed("how long does shipping take"), 1)
    assert [position for position, _ in result] == [1]
    assert type(result[0][0]) is int and type(result[0][1]) is float


def test_scores_are_the_cosine_similarities_best_first():
    index = solution.build_index(TEXTS, embed)
    query = embed("are gift cards final")
    result = solution.search(index, query, 10)
    expected = sorted(((cosine(embed(t), query), -i) for i, t in enumerate(TEXTS)), reverse=True)
    assert [position for position, _ in result] == [-negated for _, negated in expected]
    assert [score for _, score in result] == pytest.approx([score for score, _ in expected])


def test_the_querys_length_does_not_change_the_scores():
    index = solution.build_index(TEXTS, embed)
    query = embed("sale items")
    once = solution.search(index, query, 4)
    scaled = solution.search(index, query * 7.0, 4)
    assert [p for p, _ in once] == [p for p, _ in scaled]
    assert [s for _, s in once] == pytest.approx([s for _, s in scaled])


def test_equal_scores_come_in_position_order():
    index = solution.build_index(["sale items", "gift cards", "sale items"], embed)
    result = solution.search(index, embed("sale items"), 2)
    assert [position for position, _ in result] == [0, 2]
