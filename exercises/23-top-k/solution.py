import numpy as np


# ---- Given: cosine similarity, from exercise 22. Do not change. ----

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    lengths = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(a @ b) / lengths if lengths else 0.0


# ---- Yours ----

def top_k(scores: np.ndarray, k: int) -> list[int]:
    raise NotImplementedError


def most_similar(query: np.ndarray, vectors: list[np.ndarray], k: int) -> list[tuple[int, float]]:
    raise NotImplementedError
