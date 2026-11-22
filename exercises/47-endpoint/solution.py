# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---- Given. Do not change. ----


class PipelineDown(Exception):
    """The pipeline cannot answer right now (the model's API is unreachable, the index is not built)."""


async def demo_pipeline(question: str) -> tuple[str, list[str]]:
    """Stands in for the real pipeline: the same answer to every question."""
    return "You have 30 days from delivery.", ["returns.txt, page 1"]


# ---- Yours ----

# Question: a pydantic model with one field, question (a string).
class Question(BaseModel):
    pass        # replace with the field


# Reply: a pydantic model with two fields, answer (a string) and sources (a list of strings).
class Reply(BaseModel):
    pass        # replace with the fields


# create_app(pipeline): return a FastAPI app around the given async pipeline(question) -> (answer, sources), with two
# routes. GET /health answers 200 with {"status": "ok"}. POST /ask takes a Question as its JSON body, awaits
# pipeline(question) with the whitespace at the question's ends removed, and answers 200 with a Reply. A body without
# question, or one that is not a string, is 422. A question that is empty or only whitespace is 422 and the pipeline is
# not called. If the pipeline raises PipelineDown, answer 503 with {"detail": "The pipeline is not available."}.
#   POST /ask {"question": "How long do I have to return an item?"}
#     ->  200 {"answer": "You have 30 days from delivery.", "sources": ["returns.txt, page 1"]}
#   POST /ask {"question": "   "}  ->  422
def create_app(pipeline) -> FastAPI:
    raise NotImplementedError
