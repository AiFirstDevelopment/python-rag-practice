import hashlib
import re

import numpy as np


# ---- Given: a stand-in for an embedding model. Do not change. ----

def fake_embed(text: str, size: int = 64) -> np.ndarray:
    """Counts each word into one of `size` slots. The same text always gives the same vector."""
    vector = np.zeros(size)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % size] += 1.0
    return vector


# ---- Yours ----

def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    raise NotImplementedError


def build_index(texts: list[str], embed) -> np.ndarray:
    raise NotImplementedError


def search(index: np.ndarray, query: np.ndarray, k: int) -> list[tuple[int, float]]:
    raise NotImplementedError
