# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 20.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
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

# EXERCISE-TODO: format_passages(passages): return the passages as one string. Each passage is a label line, then its
# text. The label is the passage's number in square brackets (counting from 1), the file, and the page: "page 2" when
# first_page and last_page are the same, "pages 2-3" when they differ. Passages are separated by one blank line. No
# passages gives "".
#   format_passages([Passage("returns.txt", 1, 1, "Sale items ..."), Passage("gear-care.pdf", 2, 3, "Wash ...")])
#     ->  "[1] returns.txt, page 1\nSale items ...\n\n[2] gear-care.pdf, pages 2-3\nWash ..."
def format_passages(passages: list[Passage]) -> str:
    raise NotImplementedError


# EXERCISE-TODO: build_request(question, passages): return the keyword arguments of the model call as a dict with
# exactly the keys "model" (MODEL), "max_tokens" (1024), "system" (SYSTEM) and "messages": a list with one user message
# whose content is "Passages:", a blank line, the formatted passages, a blank line, and "Question: " followed by the
# question.
#   the user message's content for one passage and the question "Can I return a sale item?"
#     ->  "Passages:\n\n[1] returns.txt, page 1\nSale items ...\n\nQuestion: Can I return a sale item?"
def build_request(question: str, passages: list[Passage]) -> dict:
    raise NotImplementedError


# EXERCISE-TODO: answer(client, question, passages), async: call await client.messages.create(...) once with that
# request and return the reply's text, response.content[0].text.
async def answer(client, question: str, passages: list[Passage]) -> str:
    raise NotImplementedError
