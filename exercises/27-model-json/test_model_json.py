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
            usage=SimpleNamespace(input_tokens=200, output_tokens=12),
            stop_reason="end_turn",
        )


class FakeClient:
    """The slice of anthropic.Anthropic these exercises use: client.messages.create(...)."""

    def __init__(self, text):
        self.messages = FakeMessages(text)


PASSAGES = [
    "Shipping takes five days.",
    "Returns are accepted within 30 days.",
    "Sale items can be returned for store credit.",
    "Gift cards never expire.",
]
QUESTION = "Can I return a sale item?"
FENCE = "`" * 3


def test_strip_fence_removes_a_code_fence_and_leaves_other_text_alone():
    assert solution.strip_fence(f'{FENCE}json\n{{"ranked": [2, 0]}}\n{FENCE}') == '{"ranked": [2, 0]}'
    assert solution.strip_fence(f'\n{FENCE}\n{{"ranked": []}}\n{FENCE}\n') == '{"ranked": []}'
    assert solution.strip_fence('  {"ranked": [1]} \n') == '{"ranked": [1]}'       # no fence: only stripped


def test_parse_ranking_keeps_the_order_and_drops_repeats():
    assert solution.parse_ranking('{"ranked": [2, 0, 2, 1, 0]}', 4) == [2, 0, 1]
    assert solution.parse_ranking('{"ranked": []}', 4) == []


def test_parse_ranking_accepts_a_fenced_reply():
    assert solution.parse_ranking(f'{FENCE}json\n{{"ranked": [3, 1]}}\n{FENCE}', 4) == [3, 1]


@pytest.mark.parametrize("reply", [
    "Passage 2 is the best.",          # not JSON
    '{"ranked": [2, 0',                # cut off
    "[2, 0]",                          # not an object
    '{"order": [2, 0]}',               # no "ranked" key
    '{"ranked": "2, 0"}',              # not a list
    '{"ranked": [2, "two"]}',          # an item that is not a number
    '{"ranked": [1.5]}',               # not a whole number
])
def test_parse_ranking_refuses_a_reply_of_the_wrong_shape(reply):
    with pytest.raises(ValueError):
        solution.parse_ranking(reply, 4)


def test_parse_ranking_refuses_a_passage_it_was_not_given():
    with pytest.raises(ValueError):
        solution.parse_ranking('{"ranked": [1, 4]}', 4)
    with pytest.raises(ValueError):
        solution.parse_ranking('{"ranked": [-1]}', 4)


def test_rerank_puts_the_models_choice_first_then_the_rest_in_order():
    client = FakeClient('{"ranked": [2]}')
    assert solution.rerank(client, QUESTION, PASSAGES, keep=3) == [2, 0, 1]
    assert len(client.messages.calls) == 1
    call = client.messages.calls[0]
    assert call["system"] == solution.RULES
    assert call["messages"] == [{"role": "user", "content": solution.prompt(QUESTION, PASSAGES)}]


def test_rerank_falls_back_to_the_original_order_on_a_bad_reply():
    assert solution.rerank(FakeClient("Passage 2 is the best."), QUESTION, PASSAGES, keep=3) == [0, 1, 2]
    assert solution.rerank(FakeClient('{"ranked": [9]}'), QUESTION, PASSAGES, keep=2) == [0, 1]


def test_rerank_of_no_passages_makes_no_call():
    client = FakeClient('{"ranked": []}')
    assert solution.rerank(client, QUESTION, [], keep=3) == []
    assert client.messages.calls == []
