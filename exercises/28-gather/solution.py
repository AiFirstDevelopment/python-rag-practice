# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import asyncio

# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


# ---- Yours ----

# ask(client, question, model, max_tokens): await one call, client.messages.create(...), with the keyword arguments
# model, max_tokens, and messages holding the question as one user message, and return response.content[0].text.
async def ask(client, question: str, model: str = MODEL, max_tokens: int = 1024) -> str:
    raise NotImplementedError


# ask_all(client, questions, limit): ask every question and return the answers as a list in the order of the
# questions, whichever call finished first. The calls run at the same time, but never more than limit of them are in
# flight at once. Each question is asked once. No questions: [], no call.
#   asyncio.run(ask_all(client, ["Can I return shoes?", "How long is shipping?"], limit=5))
#     ->  ["Yes, within 30 days.", "Five days."]
async def ask_all(client, questions: list[str], limit: int = 5) -> list[str]:
    raise NotImplementedError
