# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 51.
# Write it there, save, then type /check in the Claude chat.
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel

# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"
SYSTEM = "Answer only from the passages. If the answer is not in them, say you don't know."
LOADS = {"count": 0}        # how many times load_chunks has run


def load_chunks() -> list[dict]:
    """Stands in for reading, chunking and embedding every document: slow, so the app does it once."""
    LOADS["count"] += 1
    return [
        {"text": "Returns are accepted within 30 days of delivery.", "source": "returns.txt, page 1"},
        {"text": "Sale items can be returned for store credit within 14 days.", "source": "returns.txt, page 2"},
        {"text": "Standard shipping takes five business days.", "source": "shipping.txt, page 1"},
    ]


def get_client():
    """The model client the routes depend on. The real one needs an API key; tests swap this function."""
    raise RuntimeError("No API key here. A test must swap get_client with app.dependency_overrides.")


async def pipeline(question: str, chunks: list[dict], client) -> tuple[str, list[str]]:
    """Stands in for the real pipeline: sends every chunk as a passage and returns the answer and the sources."""
    passages = "\n\n".join(f"[{chunk['source']}]\n{chunk['text']}" for chunk in chunks)
    response = await client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Passages:\n\n{passages}\n\nQuestion: {question}"}],
    )
    return response.content[0].text, [chunk["source"] for chunk in chunks]


class Question(BaseModel):
    question: str


class Reply(BaseModel):
    answer: str
    sources: list[str]


# ---- Yours ----

# create_app(): return a FastAPI app whose lifespan calls load_chunks() once when the app starts and keeps the result
# (on app.state, for example); no route calls load_chunks(). GET /health answers 200 with {"status": "ok", "chunks":
# <the number of chunks loaded>}. POST /ask takes a Question, gets the model client from Depends(get_client) (not by
# calling get_client() itself), awaits pipeline(question, chunks, client) with the chunks loaded at startup, and answers
# 200 with a Reply. A body without question is 422.
#   client.get("/health").json()  ->  {"status": "ok", "chunks": 3}
#   client.post("/ask", json={"question": "Can I return a sale item?"}).json()
#     ->  {"answer": "...", "sources": ["returns.txt, page 1", ...]}
def create_app() -> FastAPI:
    raise NotImplementedError
