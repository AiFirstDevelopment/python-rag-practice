import asyncio
import importlib.util
import json
from pathlib import Path

from fastmcp import Client

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

FILES = ["disruptions.txt", "fares.txt", "onboard.txt", "vehicles.txt"]


def run(coro):
    return asyncio.run(coro)


async def with_client(work):
    async with Client(solution.create_server()) as client:
        return await work(client)


def resources():
    return run(with_client(lambda c: c.list_resources()))


def read(uri):
    return run(with_client(lambda c: c.read_resource(uri)))[0].text


def test_the_server_is_named_ferry_docs():
    assert solution.create_server().name == "ferry-docs"


def test_every_document_is_a_resource():
    uris = {str(r.uri) for r in resources()}
    assert {f"ferry://documents/{name}" for name in FILES} <= uris


def test_document_resources_are_named_and_plain_text():
    by_uri = {str(r.uri): r for r in resources()}
    fares = by_uri["ferry://documents/fares.txt"]
    assert fares.name == "fares.txt"
    assert fares.mime_type == "text/plain"


def test_reading_a_document_gives_its_full_text():
    text = read("ferry://documents/fares.txt")
    assert text == (solution.CORPUS / "fares.txt").read_text()
    assert read("ferry://documents/vehicles.txt").startswith("Brackwater Ferry")


def test_the_catalogue_lists_the_file_names_sorted():
    by_uri = {str(r.uri): r for r in resources()}
    assert by_uri["ferry://documents"].mime_type == "application/json"
    assert json.loads(read("ferry://documents")) == FILES


def test_the_prompt_is_listed_with_its_argument():
    prompts = {p.name: p for p in run(with_client(lambda c: c.list_prompts()))}
    assert "answer_from_documents" in prompts
    assert [a.name for a in prompts["answer_from_documents"].arguments] == ["question"]


def test_the_prompt_carries_the_question_and_the_rules():
    result = run(with_client(lambda c: c.get_prompt("answer_from_documents", {"question": "Can I bring my dog?"})))
    text = " ".join(m.content.text for m in result.messages).lower()
    assert "can i bring my dog?" in text
    assert "document" in text and "cite" in text
