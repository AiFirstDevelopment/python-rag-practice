import json

from pydantic import BaseModel

# ---- Given. Do not change. ----

RERANK_MODEL = "claude-haiku-5-5"
RULES = """You choose which passages answer a question.
You are given the question and a numbered list of passages.
Reply with JSON only, in this shape: {"ranked": [2, 0]}
The numbers of the passages that answer the question, best first. An empty list if none answers it."""


def prompt(question: str, passages: list[str]) -> str:
    """The user message for the reranker: the question, then every passage with its number."""
    numbered = "\n\n".join(f"[{i}] {passage}" for i, passage in enumerate(passages))
    return f"Question: {question}\n\nPassages:\n\n{numbered}"


# ---- Yours ----

def strip_fence(text: str) -> str:
    raise NotImplementedError


def parse_ranking(text: str, pool_size: int) -> list[int]:
    raise NotImplementedError


def rerank(client, question: str, passages: list[str], keep: int = 3) -> list[int]:
    raise NotImplementedError
