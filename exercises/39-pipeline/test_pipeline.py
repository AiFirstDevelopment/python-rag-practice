import asyncio
import importlib.util
import json
import re
from pathlib import Path
from types import SimpleNamespace

import numpy as np

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

VOCAB = ["return", "refund", "sale", "credit", "ship", "express", "deliver", "tent", "wash", "warranty", "point", "gift"]

DOCUMENTS = {
    "returns.txt": [
        "Returns are accepted within 30 days of purchase with a receipt.",
        "Sale items can be returned within 14 days for store credit, not a refund.",
        "A prepaid label for return shipping is in every box.",
    ],
    "shipping.pdf": [
        "Standard shipping takes five working days and is free over 50 dollars.",
        "Express shipping costs 15 dollars and is delivered the next working day.",
        "We do not ship to post office boxes or outside the country.",
    ],
    "gear-care.pdf": [
        "Wash the tent by hand in cold water with mild soap.",
        "Dry the tent fully before you store it, or it will grow mould.",
        "Boots are cleaned with a brush and treated with wax twice a year.",
    ],
    "rewards.md": [
        "Members earn one point for every dollar spent in the store.",
        "One hundred points are worth a five dollar gift card.",
        "Points expire two years after the day they were earned.",
    ],
}


def embed(text):
    """A fake embedding: how many times each known word is in the text, plus a little so it is never all zeros."""
    return np.array([text.lower().count(word) + 0.01 for word in VOCAB])


class FakeClient:
    """Stands in for AsyncAnthropic. The reranker's call (told apart by its system prompt) gets `ranking`: the JSON
    text to reply with, or a marker, and it then names the passage holding that marker. The answer's call gets `reply`."""

    def __init__(self, reply="Express shipping costs 15 dollars.", ranking='{"ranked": [0]}'):
        self.reply, self.ranking, self.requests = reply, ranking, []
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.requests.append(request)
        text = self.reply
        if request["system"] == solution.RULES:
            text = self.ranking
            if not text.startswith("{"):
                numbered = re.findall(r"\[(\d+)\] (.*?)(?=\n\n\[\d+\] |\Z)", request["messages"][0]["content"], re.S)
                text = json.dumps({"ranked": [int(n) for n, passage in numbered if self.ranking in passage]})
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason="end_turn",
                               usage=SimpleNamespace(input_tokens=200, output_tokens=20))

    def sent_to(self, system):
        return [r for r in self.requests if r["system"] == system]


def ask(question, client, documents=DOCUMENTS):
    return asyncio.run(solution.ask(documents, question, embed, client))


def test_it_returns_the_models_reply_and_the_passages_it_answered_from():
    reply, passages = ask("How much is express shipping?", FakeClient())
    assert reply == "Express shipping costs 15 dollars."
    assert passages
    assert all(isinstance(p, solution.Passage) for p in passages)


def test_the_best_passage_is_from_the_document_that_answers_the_question():
    _, passages = ask("How much is express shipping?", FakeClient())
    assert passages[0].file == "shipping.pdf"
    assert "Express shipping costs 15 dollars" in passages[0].text
    _, passages = ask("How do I wash the tent?", FakeClient())
    assert passages[0].file == "gear-care.pdf"
    assert "Wash the tent by hand" in passages[0].text


def test_the_chosen_chunk_is_widened_with_its_neighbours():
    _, passages = ask("How much is express shipping?", FakeClient())
    assert (passages[0].first_page, passages[0].last_page) == (1, 3)
    assert "Standard shipping takes five working days" in passages[0].text
    assert "We do not ship to post office boxes" in passages[0].text


def test_there_are_two_model_calls_the_reranker_then_the_answer():
    client = FakeClient()
    ask("How much is express shipping?", client)
    assert [r["system"] for r in client.requests] == [solution.RULES, solution.SYSTEM]
    assert "Question: How much is express shipping?" in client.requests[0]["messages"][0]["content"]


def test_the_answer_is_asked_from_the_passages_that_are_returned():
    client = FakeClient()
    _, passages = ask("How much is express shipping?", client)
    [request] = client.sent_to(solution.SYSTEM)
    assert request == solution.build_request("How much is express shipping?", passages)
    assert "[1] shipping.pdf, pages 1-3" in request["messages"][0]["content"]


def test_the_rerankers_choice_goes_first():
    client = FakeClient(ranking="prepaid label")          # the reranker names the passage about the return label
    _, passages = ask("How much is express shipping?", client)
    assert passages[0].file == "returns.txt"
    assert "A prepaid label for return shipping" in passages[0].text


def test_a_reranker_reply_that_cannot_be_used_still_gives_an_answer():
    client = FakeClient(ranking="{not json")
    reply, passages = ask("How much is express shipping?", client)
    assert reply == "Express shipping costs 15 dollars."
    assert passages[0].file == "shipping.pdf"


def test_no_documents_or_only_empty_pages_is_i_dont_know_with_no_model_call():
    for documents in ({}, {"empty.pdf": ["", "  \n "]}):
        client = FakeClient()
        assert ask("How much is express shipping?", client, documents) == ("I don't know.", [])
        assert client.requests == []
