# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass

# ---- Given: the Passage, the request builder from exercise 37 and the fallback constants. Do not change them. ----

@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


MODEL = "claude-opus-5-5"
SYSTEM = ("Answer only from the passages, in a few plain sentences without Markdown. "
          "If the answer is not in them, say you don't know.")
DONT_KNOW = "I don't know."
DECLINED = "The model declined."
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")


def format_passages(passages: list[Passage]) -> str:
    return "\n\n".join(
        f"[{n}] {p.file}, " + (f"page {p.first_page}" if p.first_page == p.last_page
                               else f"pages {p.first_page}-{p.last_page}") + f"\n{p.text}"
        for n, p in enumerate(passages, 1)
    )


def build_request(question: str, passages: list[Passage]) -> dict:
    content = f"Passages:\n\n{format_passages(passages)}\n\nQuestion: {question}"
    return {"model": MODEL, "max_tokens": 1024, "system": SYSTEM, "messages": [{"role": "user", "content": content}]}


# ---- Yours ----

async def answer(client, question: str, passages: list[Passage]) -> str:
    raise NotImplementedError


def is_fallback(reply: str) -> bool:
    raise NotImplementedError
