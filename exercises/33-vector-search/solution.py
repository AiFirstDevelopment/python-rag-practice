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

def embed_chunks(chunks: list[Chunk], embed: Embed) -> np.ndarray:
    raise NotImplementedError


def nearest(vectors: np.ndarray, query: np.ndarray, limit: int) -> list[int]:
    raise NotImplementedError


def vector_search(chunks: list[Chunk], vectors: np.ndarray, question: str, embed: Embed, limit: int) -> list[Chunk]:
    raise NotImplementedError
