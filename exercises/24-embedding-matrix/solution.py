# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 19.
# Write it there, save, then type /check in the Claude chat.
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

# normalize_rows(matrix): return a new two-dimensional array where every row has length 1. A row of all zeros stays
# zeros (no nan). The array given is not changed.
def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    raise NotImplementedError


# build_index(texts, embed): embed each text with embed(text) and return the normalized matrix, one row per text, in
# order: shape (len(texts), d).
#   build_index(["returns are accepted within 30 days", "shipping takes five days", "gift cards never expire"],
#               fake_embed).shape  ->  (3, 64)
def build_index(texts: list[str], embed) -> np.ndarray:
    raise NotImplementedError


# search(index, query, k): index is a matrix from build_index; query is a one-dimensional vector of any length
# (normalize it here). Return the k best rows as a list of (position, score) tuples, a Python int and float, best
# first; equal scores in position order; all the rows if k is larger than their number. Compute the scores with one
# matrix-vector product, no Python loop over the rows.
#   search(index, fake_embed("how long does shipping take"), 1)  ->  [(1, 0.2236...)]   (index from the example above)
def search(index: np.ndarray, query: np.ndarray, k: int) -> list[tuple[int, float]]:
    raise NotImplementedError
