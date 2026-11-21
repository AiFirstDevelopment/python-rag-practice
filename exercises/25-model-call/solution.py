from dataclasses import dataclass

# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int


# ---- Yours ----

def ask(client, question: str, model: str = MODEL, max_tokens: int = 1024) -> Reply:
    raise NotImplementedError


def cost(input_tokens: int, output_tokens: int, input_price: float, output_price: float) -> float:
    raise NotImplementedError


def total_cost(replies: list[Reply], input_price: float, output_price: float) -> float:
    raise NotImplementedError
