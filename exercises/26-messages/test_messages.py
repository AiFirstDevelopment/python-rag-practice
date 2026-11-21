from types import SimpleNamespace

import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class FakeMessages:
    def __init__(self, text):
        self.text = text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=self.text)],
            usage=SimpleNamespace(input_tokens=40, output_tokens=9),
            stop_reason="end_turn",
        )


class FakeClient:
    """The slice of anthropic.Anthropic these exercises use: client.messages.create(...)."""

    def __init__(self, text="Sale items are final."):
        self.messages = FakeMessages(text)


HISTORY = [("Can I return shoes?", "Yes, within 30 days."), ("Worn ones?", "No, unworn only.")]


def test_no_history_is_one_user_message():
    assert solution.build_messages([], "Can I return shoes?") == [{"role": "user", "content": "Can I return shoes?"}]


def test_history_alternates_user_and_assistant_then_the_new_question():
    assert solution.build_messages(HISTORY, "And sale items?") == [
        {"role": "user", "content": "Can I return shoes?"},
        {"role": "assistant", "content": "Yes, within 30 days."},
        {"role": "user", "content": "Worn ones?"},
        {"role": "assistant", "content": "No, unworn only."},
        {"role": "user", "content": "And sale items?"},
    ]


def test_history_is_not_changed():
    history = list(HISTORY)
    solution.build_messages(history, "And sale items?")
    assert history == HISTORY


def test_chat_returns_the_replys_text():
    assert solution.chat(FakeClient(), "Answer in one sentence.", HISTORY, "And sale items?") == "Sale items are final."


def test_chat_sends_the_system_prompt_as_its_own_argument():
    client = FakeClient()
    solution.chat(client, "Answer in one sentence.", HISTORY, "And sale items?")
    assert len(client.messages.calls) == 1
    call = client.messages.calls[0]
    assert call["system"] == "Answer in one sentence."
    assert all(message["role"] in ("user", "assistant") for message in call["messages"])


def test_chat_sends_the_whole_conversation_model_and_max_tokens():
    client = FakeClient()
    solution.chat(client, "Answer in one sentence.", HISTORY, "And sale items?", max_tokens=300)
    call = client.messages.calls[0]
    assert len(call["messages"]) == 5
    assert call["messages"][-1] == {"role": "user", "content": "And sale items?"}
    assert call["model"] == solution.MODEL
    assert call["max_tokens"] == 300


def test_an_empty_question_raises_and_makes_no_call():
    client = FakeClient()
    with pytest.raises(ValueError):
        solution.chat(client, "Answer in one sentence.", [], "   ")
    assert client.messages.calls == []
