# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
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

# rerank(client, question, pool, keep=KEEP), async: pool is the fused chunks, best first. Return at most keep chunks.
# An empty pool returns [] without calling the model. Otherwise make one call, await client.messages.create(...), with
# model=RERANK_MODEL, max_tokens=1024, system=RULES and one user message whose content is "Question: <question>", a
# blank line, "Passages:", a blank line, then "[0] <text of pool[0]>", "[1] <text of pool[1]>", ... separated by one
# blank line. The reply's text is response.content[0].text, JSON such as {"ranked": [4, 0]}. The result is the chunks
# the model named, in its order, each once even if named twice, then the rest of the pool in pool order, cut to keep.
# Fall back to pool[:keep] when the call raises anthropic.APIError, the text is not JSON, the JSON is not an object
# with a list under "ranked", an item is not a whole number ("1" is a string), or a number is < 0 or >= len(pool).
#   pool = [Chunk("f.txt", 1, i, f"passage {i}") for i in range(6)]
#   model replies {"ranked": [4]}     ->  [pool[4], pool[0], pool[1]]
#   model replies {"ranked": [1, 9]}  ->  [pool[0], pool[1], pool[2]]
async def rerank(client, question: str, pool: list[Chunk], keep: int = KEEP) -> list[Chunk]:
    raise NotImplementedError
