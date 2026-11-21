import numpy as np
import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def test_dot_multiplies_pairs_and_adds_them_up():
    result = solution.dot(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0]))
    assert type(result) is float
    assert result == pytest.approx(32.0)


def test_same_direction_is_one_whatever_the_lengths():
    result = solution.cosine(np.array([1.0, 2.0]), np.array([10.0, 20.0]))
    assert type(result) is float
    assert result == pytest.approx(1.0)


def test_nothing_in_common_is_zero():
    assert solution.cosine(np.array([1.0, 0.0]), np.array([0.0, 2.0])) == pytest.approx(0.0)


def test_opposite_directions_is_minus_one():
    assert solution.cosine(np.array([1.0, 2.0]), np.array([-2.0, -4.0])) == pytest.approx(-1.0)


def test_a_value_in_between():
    assert solution.cosine(np.array([1.0, 0.0]), np.array([1.0, 1.0])) == pytest.approx(0.70710678)


def test_a_vector_of_zeros_scores_zero():
    assert solution.cosine(np.array([1.0, 2.0]), np.zeros(2)) == 0.0
    assert solution.cosine(np.zeros(2), np.zeros(2)) == 0.0


def test_different_shapes_raise():
    with pytest.raises(ValueError):
        solution.dot(np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]))
    with pytest.raises(ValueError):
        solution.cosine(np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]))
