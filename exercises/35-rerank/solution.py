import json
from dataclasses import dataclass

import anthropic

# ---- Given: the Chunk from exercise 31, the model and the system prompt. Do not change them. ----

@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


RERANK_MODEL = "claude-haiku-5-5"
KEEP = 3
RULES = """You choose which passages answer a question about a set of documents.
You are given the question and a numbered list of passages.
Reply with JSON only, in this shape: {"ranked": [2, 0]}
"ranked" holds the numbers of the passages that answer the question, best first.
Use an empty list if none answers it."""


# ---- Yours ----

async def rerank(client, question: str, pool: list[Chunk], keep: int = KEEP) -> list[Chunk]:
    raise NotImplementedError
