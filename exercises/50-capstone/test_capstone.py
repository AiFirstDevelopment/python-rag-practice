import asyncio
import importlib.util
import json
import re
import zlib
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

HERE = Path(__file__).parent
GOLDEN = [json.loads(line) for line in (HERE / "golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")
BUDGET = 3500       # characters: the system prompt plus every message

# The one sentence of the corpus that answers each answer case. The fake model replies with it when it was sent it.
KEY_SENTENCES = {
    "fares-01": "Children aged 5 to 15 pay half the adult fare.",
    "fares-02": "A ticket cancelled later than that is refunded as travel credit, which is valid for 12 months.",
    "fares-03": "The machine takes cards only.",
    "vehicles-01": "Vehicles must check in at least 30 minutes before departure.",
    "vehicles-02": "Spare fuel cans are not allowed in any vehicle, full or empty.",
    "onboard-01": "A dog must stay on a lead on the outer deck and is not allowed in the passenger lounge.",
    "onboard-02": "Lost property is kept at the Port Ansel ticket office for 30 days.",
    "disruptions-01": "If the company cancels a sailing, a ticket for it can be moved to any sailing in the next 7 "
                      "days or refunded in full, whichever the passenger chooses.",
}


def squeeze(text: str) -> str:
    return " ".join(text.replace("’", "'").split())


def embed(texts: list[str]) -> np.ndarray:
    """A fake embedding: each word hashed into one of 64 slots, the row scaled to length 1."""
    embed.calls += 1
    rows = np.zeros((len(texts), 64))
    for row, text in zip(rows, texts):
        for word in re.findall(r"[a-z0-9']+", text.lower()):
            row[zlib.crc32(word.encode()) % 64] += 1
        length = np.linalg.norm(row)
        if length:
            row /= length
    return rows


embed.calls = 0


class FakeMessages:
    def __init__(self):
        self.calls = 0

    async def create(self, *, model, max_tokens, messages, system="", **_):
        self.calls += 1
        assert isinstance(system, str), "pass system as a plain string"
        assert all(isinstance(m["content"], str) for m in messages), "pass each message's content as a plain string"
        size = len(system) + sum(len(m["content"]) for m in messages)
        if size > BUDGET:
            raise ValueError(f"the prompt is {size} characters; the budget is {BUDGET}")
        user = squeeze(" ".join(m["content"] for m in messages if m["role"] == "user"))
        case = next((c for c in GOLDEN if squeeze(c["question"]) in user), None)
        assert case is not None, "the user message must contain the question, word for word"
        key = KEY_SENTENCES.get(case["id"])
        told_to_fall_back = any(phrase in squeeze(system).lower() for phrase in ("don't know", "do not know"))
        if key and squeeze(key) in user:
            text = key
        elif told_to_fall_back:
            text = "I don't know."
        else:
            text = "Yes, that is fine. It costs $12."        # nothing told it not to guess
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=text)],
            stop_reason="end_turn",
            usage=SimpleNamespace(input_tokens=size // 4, output_tokens=len(text) // 4),
        )


class FakeClient:
    def __init__(self):
        self.messages = FakeMessages()


@pytest.fixture(scope="module")
def pipeline():
    path = HERE / "pipeline.py"
    if not path.exists():
        pytest.fail("there is no pipeline.py in exercises/50-capstone yet: see the README")
    spec = importlib.util.spec_from_file_location("capstone_pipeline", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def score(case: dict, reply: str) -> tuple[str, list[str]]:
    text = reply.lower()
    if case["expected_behavior"] == "fallback":
        return ("pass" if any(phrase in text for phrase in FALLBACK) else "review"), []
    missing = [f["fact"] for f in case["required_facts"] if not any(m.lower() in text for m in f["match"])]
    return ("fail" if missing else "pass"), missing


@pytest.mark.parametrize("case", GOLDEN, ids=[c["id"] for c in GOLDEN])
def test_golden_case_passes(pipeline, case):
    reply = asyncio.run(pipeline.answer(case["question"], FakeClient(), embed))
    assert isinstance(reply, str)
    status, missing = score(case, reply)
    assert status == "pass", f"{case['id']}: {status}; the reply was {reply!r}; missing facts: {missing}"


def test_one_model_call_per_question(pipeline):
    client = FakeClient()
    asyncio.run(pipeline.answer(GOLDEN[0]["question"], client, embed))
    assert client.messages.calls == 1


def test_the_embed_function_is_used(pipeline):
    before = embed.calls
    asyncio.run(pipeline.answer(GOLDEN[0]["question"], FakeClient(), embed))
    assert embed.calls > before
