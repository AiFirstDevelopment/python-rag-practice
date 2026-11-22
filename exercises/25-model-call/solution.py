# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass

# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int


# ---- Yours ----

# ask(client, question, model, max_tokens): make one call, client.messages.create(...), with the keyword arguments
# model, max_tokens, and messages as a list holding one message, {"role": "user", "content": question}. Return a
# Reply with the text (response.content[0].text) and the two token counts (response.usage.input_tokens and
# response.usage.output_tokens).
#   ask(client, "How long do I have to return an item?")  ->  Reply(text="30 days from delivery.", input_tokens=18, ...)
def ask(client, question: str, model: str = MODEL, max_tokens: int = 1024) -> Reply:
    raise NotImplementedError


# cost(input_tokens, output_tokens, input_price, output_price): return the dollars one call cost. The prices are
# dollars per million tokens.
#   cost(1_000_000, 0, 5.0, 25.0)  ->  5.0
#   cost(2_000, 500, 5.0, 25.0)    ->  0.0225
def cost(input_tokens: int, output_tokens: int, input_price: float, output_price: float) -> float:
    raise NotImplementedError


# total_cost(replies, input_price, output_price): return the dollars for a list of Reply; 0.0 for an empty list.
def total_cost(replies: list[Reply], input_price: float, output_price: float) -> float:
    raise NotImplementedError
