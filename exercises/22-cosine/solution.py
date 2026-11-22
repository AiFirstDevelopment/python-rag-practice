# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
import numpy as np


# EXERCISE-TODO: dot(a, b): return the dot product of two one-dimensional arrays (each pair of numbers multiplied, the
# products added up) as a Python float. Raise ValueError when the two arrays do not have the same shape.
#   dot(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0]))  ->  32.0
def dot(a: np.ndarray, b: np.ndarray) -> float:
    raise NotImplementedError


# EXERCISE-TODO: cosine(a, b): return the dot product divided by the two lengths multiplied together, as a Python float.
# If either vector is all zeros, return 0.0 (no division by zero, no nan). Raise ValueError when the two arrays do not
# have the same shape.
#   cosine(np.array([1.0, 0.0]), np.array([5.0, 0.0]))  ->  1.0
#   cosine(np.array([1.0, 0.0]), np.zeros(2))           ->  0.0
def cosine(a: np.ndarray, b: np.ndarray) -> float:
    raise NotImplementedError
