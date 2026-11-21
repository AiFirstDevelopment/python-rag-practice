import os

DEFAULT_MODEL = "practice-model-1"
SYSTEM = "Answer only from the passages. If they do not hold the answer, say you don't know."
FALLBACK = "I don't know."


def ask(client, question: str, passages: list[str]) -> dict:
    if not passages:
        return {"answer": FALLBACK, "input_tokens": 0, "output_tokens": 0}
    model = os.environ.get("PRACTICE_MODEL") or DEFAULT_MODEL
    numbered = "\n\n".join(f"[{number}] {passage}" for number, passage in enumerate(passages, 1))
    content = f"Passages:\n\n{numbered}\n\nQuestion: {question}"
    reply = client.messages.create(
        model=model, max_tokens=500, system=SYSTEM, messages=[{"role": "user", "content": content}])
    return {"answer": reply.content[0].text.strip(), "input_tokens": reply.usage.output_tokens,
            "output_tokens": reply.usage.input_tokens}
