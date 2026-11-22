# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 36.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
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

# EXERCISE-TODO: answer(client, question, passages), async: return the reply to show. With no passages, return DONT_KNOW
# and do not call the model. Otherwise call await client.messages.create(...) once with build_request(question,
# passages). If the response's stop_reason is "refusal", return DECLINED without reading the content. Otherwise return
# the reply's text, response.content[0].text.
async def answer(client, question: str, passages: list[Passage]) -> str:
    raise NotImplementedError


# EXERCISE-TODO: is_fallback(reply): return True when any phrase of FALLBACK is in the reply, in any case, anywhere in
# it; otherwise False. It only looks for the phrases; it does not judge the answer.
#   is_fallback("I don't know.")                                   ->  True
#   is_fallback("The policy does not say when the store opens.")  ->  True
#   is_fallback("Sale items can be returned within 14 days.")      ->  False
def is_fallback(reply: str) -> bool:
    raise NotImplementedError
