import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

PASSAGES = [solution.Passage("returns.txt", 1, 1, "Sale items can be returned for store credit.")]


class FakeClient:
    """Stands in for AsyncAnthropic: messages.create records the request and returns the scripted reply."""

    def __init__(self, text="", stop_reason="end_turn"):
        self.text, self.stop_reason, self.requests = text, stop_reason, []
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.requests.append(request)
        content = [] if self.stop_reason == "refusal" else [SimpleNamespace(type="text", text=self.text)]
        return SimpleNamespace(content=content, stop_reason=self.stop_reason,
                               usage=SimpleNamespace(input_tokens=120, output_tokens=15))


def ask(client, passages=PASSAGES):
    return asyncio.run(solution.answer(client, "Can I return a sale item?", passages))


def test_no_passages_answers_i_dont_know_without_calling_the_model():
    client = FakeClient("Yes.")
    assert ask(client, passages=[]) == "I don't know."
    assert client.requests == []


def test_with_passages_the_models_reply_comes_back():
    client = FakeClient("Yes, for store credit.")
    assert ask(client) == "Yes, for store credit."


def test_the_model_is_called_once_with_the_request_from_build_request():
    client = FakeClient("Yes, for store credit.")
    ask(client)
    assert client.requests == [solution.build_request("Can I return a sale item?", PASSAGES)]
    assert "say you don't know" in client.requests[0]["system"]


def test_a_refusal_answers_that_the_model_declined():
    assert ask(FakeClient(stop_reason="refusal")) == "The model declined."


def test_the_models_own_i_dont_know_is_a_fallback():
    reply = ask(FakeClient("I don't know. The passages cover returns, not opening hours."))
    assert solution.is_fallback(reply) is True


def test_every_fallback_phrase_counts_in_any_case():
    assert solution.is_fallback("I DON'T KNOW.") is True
    assert solution.is_fallback("Sorry, I do not know that.") is True
    assert solution.is_fallback("That is not in the passages.") is True
    assert solution.is_fallback("The returns policy doesn't say.") is True
    assert solution.is_fallback("The policy does not say when the store opens.") is True


def test_an_answer_is_not_a_fallback():
    assert solution.is_fallback("Sale items can be returned within 14 days for store credit.") is False
    assert solution.is_fallback("") is False


def test_the_reply_for_no_passages_is_itself_a_fallback():
    assert solution.is_fallback(ask(FakeClient(), passages=[])) is True
