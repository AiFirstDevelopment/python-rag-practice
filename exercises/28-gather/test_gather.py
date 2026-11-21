import asyncio
from types import SimpleNamespace

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class FakeAsyncMessages:
    def __init__(self, delays):
        self.delays = delays
        self.calls = []
        self.in_flight = 0
        self.most_in_flight = 0

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        question = kwargs["messages"][-1]["content"]
        self.in_flight += 1
        self.most_in_flight = max(self.most_in_flight, self.in_flight)
        await asyncio.sleep(self.delays.get(question, 0.01))
        self.in_flight -= 1
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=f"Answer to: {question}")],
            usage=SimpleNamespace(input_tokens=12, output_tokens=6),
            stop_reason="end_turn",
        )


class FakeAsyncClient:
    """The slice of anthropic.AsyncAnthropic these exercises use: await client.messages.create(...).
    It counts how many calls are waiting at the same moment."""

    def __init__(self, delays=None):
        self.messages = FakeAsyncMessages(delays or {})


QUESTIONS = [f"Question {n}?" for n in range(8)]


def test_ask_awaits_one_call_and_returns_the_text():
    client = FakeAsyncClient()
    assert asyncio.run(solution.ask(client, "Can I return shoes?")) == "Answer to: Can I return shoes?"
    assert len(client.messages.calls) == 1
    call = client.messages.calls[0]
    assert call["messages"] == [{"role": "user", "content": "Can I return shoes?"}]
    assert call["model"] == solution.MODEL
    assert call["max_tokens"] == 1024


def test_answers_come_back_in_the_order_of_the_questions():
    client = FakeAsyncClient(delays={"Question 0?": 0.05, "Question 1?": 0.03})     # the first ones finish last
    answers = asyncio.run(solution.ask_all(client, QUESTIONS, limit=8))
    assert answers == [f"Answer to: {question}" for question in QUESTIONS]


def test_the_calls_run_at_the_same_time():
    client = FakeAsyncClient()
    asyncio.run(solution.ask_all(client, QUESTIONS, limit=4))
    assert client.messages.most_in_flight == 4


def test_never_more_than_the_limit_in_flight():
    client = FakeAsyncClient()
    asyncio.run(solution.ask_all(client, QUESTIONS, limit=3))
    assert 1 < client.messages.most_in_flight <= 3


def test_a_limit_of_one_runs_them_one_at_a_time_and_still_answers_all():
    client = FakeAsyncClient()
    answers = asyncio.run(solution.ask_all(client, QUESTIONS[:3], limit=1))
    assert client.messages.most_in_flight == 1
    assert answers == [f"Answer to: {question}" for question in QUESTIONS[:3]]


def test_each_question_is_asked_once():
    client = FakeAsyncClient()
    asyncio.run(solution.ask_all(client, QUESTIONS, limit=5))
    asked = sorted(call["messages"][-1]["content"] for call in client.messages.calls)
    assert asked == sorted(QUESTIONS)


def test_no_questions_makes_no_call():
    client = FakeAsyncClient()
    assert asyncio.run(solution.ask_all(client, [], limit=5)) == []
    assert client.messages.calls == []
