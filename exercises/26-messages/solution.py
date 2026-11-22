# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 8.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
# ---- Given. Do not change. ----

MODEL = "claude-opus-5-5"


# ---- Yours ----

# EXERCISE-TODO: build_messages(history, question): history is a list of (question, answer) tuples, oldest first. Return
# a new list of dicts: for each pair {"role": "user", "content": question} then {"role": "assistant", "content":
# answer}, and last the new question as a user message. history is not changed.
#   build_messages([("Can I return shoes?", "Yes, within 30 days.")], "And sale items?")
#     ->  [{"role": "user", "content": "Can I return shoes?"},
#          {"role": "assistant", "content": "Yes, within 30 days."},
#          {"role": "user", "content": "And sale items?"}]
def build_messages(history: list[tuple[str, str]], question: str) -> list[dict]:
    raise NotImplementedError


# EXERCISE-TODO: chat(client, system, history, question, model, max_tokens): call client.messages.create(...) once with
# the keyword arguments model, max_tokens, system (the string given) and messages (from build_messages), and return the
# reply's text, response.content[0].text. No message has the role system. If question is empty or only whitespace, raise
# ValueError without calling the client.
#   chat(client, "Answer in one sentence.", [], "Can I return shoes?")  ->  "Yes, within 30 days."
def chat(client, system: str, history: list[tuple[str, str]], question: str,
         model: str = MODEL, max_tokens: int = 1024) -> str:
    raise NotImplementedError
