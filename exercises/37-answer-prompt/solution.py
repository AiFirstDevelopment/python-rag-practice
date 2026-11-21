from dataclasses import dataclass

# ---- Given: the Passage from exercise 36, the model and the system prompt. Do not change them. ----

@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


MODEL = "claude-opus-5-5"
SYSTEM = ("Answer only from the passages, in a few plain sentences without Markdown. "
          "If the answer is not in them, say you don't know.")


# ---- Yours ----

def format_passages(passages: list[Passage]) -> str:
    raise NotImplementedError


def build_request(question: str, passages: list[Passage]) -> dict:
    raise NotImplementedError


async def answer(client, question: str, passages: list[Passage]) -> str:
    raise NotImplementedError
