# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 13.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
import numpy as np


# ---- Given: cosine similarity, from exercise 22. Do not change. ----

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    lengths = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(a @ b) / lengths if lengths else 0.0


# ---- Yours ----

# EXERCISE-TODO: top_k(scores, k): scores is a one-dimensional array. Return the positions of the k highest scores as a
# list of Python ints, highest score first. When two scores are equal, the lower position comes first. If k is larger
# than the number of scores, return all the positions; if k is 0 or less, return [].
#   top_k(np.array([0.1, 0.9, 0.4, 0.9]), 3)  ->  [1, 3, 2]
def top_k(scores: np.ndarray, k: int) -> list[int]:
    raise NotImplementedError


# EXERCISE-TODO: most_similar(query, vectors, k): vectors is a list of arrays. Return the k vectors most similar to
# query by cosine similarity as a list of (position, score) tuples, best first, with the same rules as top_k; each score
# a Python float.
#   most_similar(np.array([1.0, 0.0]), [np.array([0.0, 1.0]), np.array([2.0, 0.0]), np.array([1.0, 1.0])], 2)
#     ->  [(1, 1.0), (2, 0.7071...)]
def most_similar(query: np.ndarray, vectors: list[np.ndarray], k: int) -> list[tuple[int, float]]:
    raise NotImplementedError
