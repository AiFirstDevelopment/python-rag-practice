# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import numpy as np


# to_vector(values): return a one-dimensional array of floats (dtype float64) holding values, also when the values
# given are whole numbers.
#   to_vector([3, 4])  ->  array([3., 4.])
def to_vector(values: list[float]) -> np.ndarray:
    raise NotImplementedError


# length(v): return the vector's length (the square root of the sum of its squares) as a Python float.
#   length(to_vector([3, 4]))  ->  5.0
def length(v: np.ndarray) -> float:
    raise NotImplementedError


# normalize(v): return a new array pointing the same way with length 1. A vector of all zeros returns zeros, never
# nan. The array given is not changed.
#   normalize(to_vector([3, 4]))  ->  array([0.6, 0.8])
def normalize(v: np.ndarray) -> np.ndarray:
    raise NotImplementedError


# stack(rows): return a two-dimensional array with one row per list: n lists of d numbers give the shape (n, d).
# Raise ValueError if the lists are not all the same length.
#   stack([[1, 2, 3], [4, 5, 6]]).shape  ->  (2, 3)
def stack(rows: list[list[float]]) -> np.ndarray:
    raise NotImplementedError


# mean_vector(matrix): return the average row of a two-dimensional array: a one-dimensional array of d numbers, the
# mean of each column.
#   mean_vector(stack([[1, 2], [3, 6]]))  ->  array([2., 4.])
def mean_vector(matrix: np.ndarray) -> np.ndarray:
    raise NotImplementedError
