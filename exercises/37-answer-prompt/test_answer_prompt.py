import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Passage = solution.Passage
RETURNS = Passage("returns.txt", 1, 1, "Sale items can be returned for store credit.")
CARE = Passage("gear-care.pdf", 2, 3, "Wash the tent by hand.\nDry it before storing it.")


class FakeClient:
    """Stands in for AsyncAnthropic: messages.create records the request and returns the scripted text."""

    def __init__(self, text):
        self.text, self.requests = text, []
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.requests.append(request)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.text)], stop_reason="end_turn",
                               usage=SimpleNamespace(input_tokens=120, output_tokens=15))


def test_a_passage_is_a_numbered_label_with_file_and_page_then_its_text():
    assert solution.format_passages([RETURNS]) == "[1] returns.txt, page 1\nSale items can be returned for store credit."


def test_a_passage_over_several_pages_says_pages_and_the_range():
    assert solution.format_passages([CARE]) == "[1] gear-care.pdf, pages 2-3\nWash the tent by hand.\nDry it before storing it."


def test_passages_are_numbered_from_one_and_separated_by_a_blank_line():
    assert solution.format_passages([RETURNS, CARE]) == (
        "[1] returns.txt, page 1\nSale items can be returned for store credit.\n\n"
        "[2] gear-care.pdf, pages 2-3\nWash the tent by hand.\nDry it before storing it."
    )


def test_no_passages_formats_to_an_empty_string():
    assert solution.format_passages([]) == ""


def test_the_request_has_the_model_the_limit_and_the_system_prompt():
    request = solution.build_request("Can I return a sale item?", [RETURNS])
    assert set(request) == {"model", "max_tokens", "system", "messages"}
    assert request["model"] == solution.MODEL
    assert request["max_tokens"] == 1024
    assert request["system"] == solution.SYSTEM


def test_the_user_message_holds_the_passages_then_the_question():
    request = solution.build_request("Can I return a sale item?", [RETURNS])
    assert request["messages"] == [{
        "role": "user",
        "content": "Passages:\n\n[1] returns.txt, page 1\nSale items can be returned for store credit.\n\n"
                   "Question: Can I return a sale item?",
    }]


def test_answer_sends_that_request_once_and_returns_the_reply_text():
    client = FakeClient("Yes, for store credit.")
    reply = asyncio.run(solution.answer(client, "Can I return a sale item?", [RETURNS, CARE]))
    assert reply == "Yes, for store credit."
    assert client.requests == [solution.build_request("Can I return a sale item?", [RETURNS, CARE])]
