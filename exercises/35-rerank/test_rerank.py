import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import anthropic
import httpx

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Chunk = solution.Chunk
POOL = [Chunk("f.txt", 1, i, f"passage {i}") for i in range(6)]


class FakeClient:
    """Stands in for AsyncAnthropic: messages.create returns the scripted text, or raises the scripted error."""

    def __init__(self, text="", error=None):
        self.text, self.error, self.requests = text, error, []
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.requests.append(request)
        if self.error:
            raise self.error
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.text)],
                               usage=SimpleNamespace(input_tokens=50, output_tokens=5))


def run(text="", error=None, pool=POOL, **options):
    client = FakeClient(text, error)
    return asyncio.run(solution.rerank(client, "Can I get a refund?", pool, **options)), client


def test_the_models_choice_goes_first_then_the_pool_in_order():
    result, _ = run('{"ranked": [4]}')
    assert result == [POOL[4], POOL[0], POOL[1]]


def test_keep_sets_how_many_come_back():
    result, _ = run('{"ranked": [5, 2]}', keep=4)
    assert result == [POOL[5], POOL[2], POOL[0], POOL[1]]
    result, _ = run('{"ranked": [5, 2, 3]}', keep=2)
    assert result == [POOL[5], POOL[2]]


def test_a_passage_named_twice_counts_once():
    result, _ = run('{"ranked": [2, 2, 5]}')
    assert result == [POOL[2], POOL[5], POOL[0]]


def test_the_request_holds_the_question_the_numbered_passages_and_the_rules():
    _, client = run('{"ranked": []}')
    [request] = client.requests
    assert request["model"] == solution.RERANK_MODEL
    assert request["system"] == solution.RULES
    [message] = request["messages"]
    assert message["role"] == "user"
    assert "Question: Can I get a refund?" in message["content"]
    assert "[0] passage 0\n\n[1] passage 1" in message["content"]
    assert "[5] passage 5" in message["content"]


def test_a_number_outside_the_pool_falls_back_to_fusion_order():
    assert run('{"ranked": [1, 9]}')[0] == POOL[:3]
    assert run('{"ranked": [6]}')[0] == POOL[:3]
    assert run('{"ranked": [-1]}')[0] == POOL[:3]


def test_a_reply_that_is_not_the_asked_for_json_falls_back():
    assert run("Passage 4 answers it best.")[0] == POOL[:3]
    assert run('{"order": [4]}')[0] == POOL[:3]
    assert run('{"ranked": "4"}')[0] == POOL[:3]
    assert run('{"ranked": ["4"]}')[0] == POOL[:3]
    assert run("[4]")[0] == POOL[:3]


def test_a_failed_call_falls_back_to_fusion_order():
    error = anthropic.APIConnectionError(request=httpx.Request("POST", "https://example.test"))
    result, client = run(error=error)
    assert result == POOL[:3]
    assert len(client.requests) == 1


def test_an_empty_pool_gives_nothing_and_calls_nothing():
    result, client = run('{"ranked": [0]}', pool=[])
    assert result == []
    assert client.requests == []
