import numpy as np


def to_vector(values: list[float]) -> np.ndarray:
    raise NotImplementedError


def length(v: np.ndarray) -> float:
    raise NotImplementedError


def normalize(v: np.ndarray) -> np.ndarray:
    raise NotImplementedError


def stack(rows: list[list[float]]) -> np.ndarray:
    raise NotImplementedError


def mean_vector(matrix: np.ndarray) -> np.ndarray:
    raise NotImplementedError
