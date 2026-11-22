# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

# ---- Given: the Chunk from exercise 31. Do not change it. ----

@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


Embed = Callable[[str], np.ndarray]          # a function from a text to its vector


# ---- Yours ----

# embed_chunks(chunks, embed): return a 2-D array with one row per chunk, in order: row i is embed of chunk i's text.
def embed_chunks(chunks: list[Chunk], embed: Embed) -> np.ndarray:
    raise NotImplementedError


# nearest(vectors, query, limit): return the indexes of the rows of vectors most like query, by cosine similarity,
# best first, at most limit of them, as a list of plain Python ints (not NumPy integers). The rows are not
# normalized: a long vector must not win for being long. A limit larger than the number of rows gives all of them.
# The order of rows with equal scores is not tested.
#   nearest(np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]]), np.array([1.0, 0.1]), 2)  ->  [0, 2]
def nearest(vectors: np.ndarray, query: np.ndarray, limit: int) -> list[int]:
    raise NotImplementedError


# vector_search(chunks, vectors, question, embed, limit): embed the question and return the limit chunks nearest to
# it, best first, where vectors is what embed_chunks returned for these chunks. Return the Chunk objects themselves.
# No chunks gives [] without calling embed. A limit larger than the number of chunks gives all of them.
def vector_search(chunks: list[Chunk], vectors: np.ndarray, question: str, embed: Embed, limit: int) -> list[Chunk]:
    raise NotImplementedError
