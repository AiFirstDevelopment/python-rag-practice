import numpy as np
import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def test_to_vector_is_one_dimensional_floats_even_from_whole_numbers():
    v = solution.to_vector([3, 4])
    assert isinstance(v, np.ndarray)
    assert v.shape == (2,)
    assert v.dtype == np.float64
    assert np.allclose(v, [3.0, 4.0])


def test_length_is_a_python_float():
    result = solution.length(np.array([3.0, 4.0]))
    assert type(result) is float
    assert result == pytest.approx(5.0)


def test_normalize_gives_length_one_in_the_same_direction():
    unit = solution.normalize(np.array([3.0, 4.0]))
    assert np.allclose(unit, [0.6, 0.8])
    assert np.linalg.norm(unit) == pytest.approx(1.0)


def test_normalize_of_zeros_is_zeros_not_nan():
    unit = solution.normalize(np.zeros(3))
    assert unit.shape == (3,)
    assert not np.isnan(unit).any()
    assert np.allclose(unit, [0.0, 0.0, 0.0])


def test_normalize_does_not_change_the_array_given():
    v = np.array([3.0, 4.0])
    solution.normalize(v)
    assert np.allclose(v, [3.0, 4.0])


def test_stack_makes_one_row_per_list():
    matrix = solution.stack([[1, 2, 3], [4, 5, 6]])
    assert matrix.shape == (2, 3)
    assert np.allclose(matrix[1], [4.0, 5.0, 6.0])


def test_stack_refuses_rows_of_different_lengths():
    with pytest.raises(ValueError):
        solution.stack([[1, 2, 3], [4, 5]])


def test_mean_vector_averages_each_column():
    mean = solution.mean_vector(np.array([[1.0, 2.0], [3.0, 6.0]]))
    assert mean.shape == (2,)
    assert np.allclose(mean, [2.0, 4.0])
