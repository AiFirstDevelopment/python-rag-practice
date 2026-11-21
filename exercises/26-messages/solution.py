# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


# ---- Yours ----

def build_messages(history: list[tuple[str, str]], question: str) -> list[dict]:
    raise NotImplementedError


def chat(client, system: str, history: list[tuple[str, str]], question: str,
         model: str = MODEL, max_tokens: int = 1024) -> str:
    raise NotImplementedError
