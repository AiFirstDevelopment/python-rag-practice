from types import SimpleNamespace

import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class FakeMessages:
    def __init__(self, text, input_tokens, output_tokens):
        self.text, self.input_tokens, self.output_tokens = text, input_tokens, output_tokens
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=self.text)],
            usage=SimpleNamespace(input_tokens=self.input_tokens, output_tokens=self.output_tokens),
            stop_reason="end_turn",
        )


class FakeClient:
    """The slice of anthropic.Anthropic these exercises use: client.messages.create(...)."""

    def __init__(self, text="30 days from delivery.", input_tokens=18, output_tokens=7):
        self.messages = FakeMessages(text, input_tokens, output_tokens)


def test_ask_returns_the_text_and_both_token_counts():
    reply = solution.ask(FakeClient(), "How long do I have to return an item?")
    assert isinstance(reply, solution.Reply)
    assert reply.text == "30 days from delivery."
    assert reply.input_tokens == 18
    assert reply.output_tokens == 7


def test_ask_sends_the_question_as_one_user_message():
    client = FakeClient()
    solution.ask(client, "How long do I have to return an item?")
    assert len(client.messages.calls) == 1
    assert client.messages.calls[0]["messages"] == [
        {"role": "user", "content": "How long do I have to return an item?"}]


def test_ask_uses_the_default_model_and_max_tokens():
    client = FakeClient()
    solution.ask(client, "Hello")
    assert client.messages.calls[0]["model"] == solution.MODEL
    assert client.messages.calls[0]["max_tokens"] == 1024


def test_ask_passes_a_model_and_max_tokens_given():
    client = FakeClient()
    solution.ask(client, "Hello", model="claude-haiku-5-5", max_tokens=200)
    assert client.messages.calls[0]["model"] == "claude-haiku-5-5"
    assert client.messages.calls[0]["max_tokens"] == 200


def test_cost_prices_are_per_million_tokens():
    assert solution.cost(1_000_000, 0, 5.0, 25.0) == pytest.approx(5.0)
    assert solution.cost(0, 1_000_000, 5.0, 25.0) == pytest.approx(25.0)
    assert solution.cost(2_000, 500, 5.0, 25.0) == pytest.approx(0.0225)


def test_total_cost_adds_up_every_reply():
    replies = [solution.Reply("a", 2_000, 500), solution.Reply("b", 1_000, 100)]
    assert solution.total_cost(replies, 5.0, 25.0) == pytest.approx(0.0225 + 0.0075)


def test_total_cost_of_no_replies_is_zero():
    assert solution.total_cost([], 5.0, 25.0) == 0.0
