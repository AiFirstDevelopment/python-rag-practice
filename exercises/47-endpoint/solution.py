from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---- Given. Do not change. ----


class PipelineDown(Exception):
    """The pipeline cannot answer right now (the model's API is unreachable, the index is not built)."""


async def demo_pipeline(question: str) -> tuple[str, list[str]]:
    """Stands in for the real pipeline: the same answer to every question."""
    return "You have 30 days from delivery.", ["returns.txt, page 1"]


# ---- Yours ----

class Question(BaseModel):
    pass        # replace with the field


class Reply(BaseModel):
    pass        # replace with the fields


def create_app(pipeline) -> FastAPI:
    raise NotImplementedError
