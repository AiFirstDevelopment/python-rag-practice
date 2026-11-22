# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 22.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
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

# EXERCISE-TODO: strip_fence(text): return the text without whitespace at the ends and, if it is wrapped in a Markdown
# code fence (a first line starting with three backticks, with or without the word json, and a last line of three
# backticks), without those two lines. Text with no fence comes back stripped, otherwise unchanged.
#   strip_fence('```json\n{"ranked": [2, 0]}\n```')  ->  '{"ranked": [2, 0]}'
def strip_fence(text: str) -> str:
    raise NotImplementedError


# EXERCISE-TODO: parse_ranking(text, pool_size): return the list of passage numbers in the reply, in the reply's order,
# repeats dropped (the first one stays). Accept a fenced reply. Raise ValueError when:
#   the text is not JSON;
#   the JSON is not an object with the key "ranked";
#   "ranked" is not a list, or an item in it is not a whole number ("two", 1.5);
#   a number is less than 0 or not less than pool_size.
#   parse_ranking('{"ranked": [2, 0, 2]}', 4)    ->  [2, 0]
#   parse_ranking('{"ranked": [7]}', 4)          ->  ValueError
#   parse_ranking("Passage 2 is the best.", 4)   ->  ValueError
def parse_ranking(text: str, pool_size: int) -> list[int]:
    raise NotImplementedError


# EXERCISE-TODO: rerank(client, question, passages, keep): return keep passage positions, best first. With no passages
# return [] and make no call. Otherwise make one call, client.messages.create(model=RERANK_MODEL, max_tokens=1024,
# system=RULES, messages=[...]), with one user message whose content is prompt(question, passages), and parse
# response.content[0].text with parse_ranking. The model's choice goes first, then the positions it did not name in
# their original order, and the list is cut to keep. If parse_ranking raises ValueError, return the first keep
# positions in their original order.
#   four passages, the model replies {"ranked": [2]}:
#     rerank(client, "Can I return a sale item?", passages, keep=3)  ->  [2, 0, 1]
#   the model replies "Passage 2 is the best.":
#     rerank(client, "Can I return a sale item?", passages, keep=3)  ->  [0, 1, 2]
def rerank(client, question: str, passages: list[str], keep: int = 3) -> list[int]:
    raise NotImplementedError
