import numpy as np
import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def test_positions_of_the_highest_scores_best_first():
    assert solution.top_k(np.array([0.1, 0.9, 0.4, 0.7]), 2) == [1, 3]


def test_positions_are_python_ints():
    result = solution.top_k(np.array([0.1, 0.9, 0.4]), 2)
    assert all(type(i) is int for i in result)


def test_equal_scores_come_in_position_order():
    assert solution.top_k(np.array([0.1, 0.9, 0.4, 0.9]), 3) == [1, 3, 2]
    assert solution.top_k(np.array([0.5, 0.5, 0.5, 0.5]), 2) == [0, 1]


def test_k_larger_than_the_scores_returns_them_all():
    assert solution.top_k(np.array([0.2, 0.3, 0.1]), 10) == [1, 0, 2]


def test_k_of_zero_or_less_returns_nothing():
    assert solution.top_k(np.array([0.2, 0.3]), 0) == []
    assert solution.top_k(np.array([0.2, 0.3]), -1) == []


def test_most_similar_gives_positions_with_their_scores():
    vectors = [np.array([0.0, 1.0]), np.array([2.0, 0.0]), np.array([1.0, 1.0])]
    result = solution.most_similar(np.array([1.0, 0.0]), vectors, 2)
    assert [position for position, _ in result] == [1, 2]
    assert result[0][1] == pytest.approx(1.0)
    assert result[1][1] == pytest.approx(0.70710678)
    assert all(type(position) is int and type(score) is float for position, score in result)


def test_most_similar_keeps_equal_vectors_in_position_order():
    vectors = [np.array([0.0, 3.0]), np.array([1.0, 0.0]), np.array([4.0, 0.0])]
    result = solution.most_similar(np.array([2.0, 0.0]), vectors, 3)
    assert [position for position, _ in result] == [1, 2, 0]


def test_most_similar_of_no_vectors():
    assert solution.most_similar(np.array([1.0, 0.0]), [], 3) == []
