# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import asyncio

# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


# ---- Yours ----

async def ask(client, question: str, model: str = MODEL, max_tokens: int = 1024) -> str:
    raise NotImplementedError


async def ask_all(client, questions: list[str], limit: int = 5) -> list[str]:
    raise NotImplementedError
