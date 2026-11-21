from types import SimpleNamespace

from fastapi.testclient import TestClient

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class FakeAsyncMessages:
    def __init__(self, text):
        self.text = text
        self.calls = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=self.text)],
            usage=SimpleNamespace(input_tokens=120, output_tokens=15),
            stop_reason="end_turn",
        )


class FakeAsyncClient:
    """The slice of anthropic.AsyncAnthropic the pipeline uses: await client.messages.create(...)."""

    def __init__(self, text="Sale items can be returned for store credit."):
        self.messages = FakeAsyncMessages(text)


def app_with(fake):
    app = solution.create_app()
    app.dependency_overrides[solution.get_client] = lambda: fake
    return app


def test_health_reports_the_chunks_loaded_at_startup():
    with TestClient(app_with(FakeAsyncClient())) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "chunks": 3}


def test_the_chunks_are_loaded_once_however_many_requests_come():
    before = solution.LOADS["count"]
    with TestClient(app_with(FakeAsyncClient())) as client:
        assert solution.LOADS["count"] == before + 1        # loaded at startup, before any request
        client.get("/health")
        client.post("/ask", json={"question": "Can I return a sale item?"})
        client.post("/ask", json={"question": "How long is shipping?"})
    assert solution.LOADS["count"] == before + 1


def test_creating_the_app_loads_nothing():
    before = solution.LOADS["count"]
    solution.create_app()
    assert solution.LOADS["count"] == before


def test_ask_answers_through_the_swapped_client():
    with TestClient(app_with(FakeAsyncClient("Sale items can be returned for store credit."))) as client:
        response = client.post("/ask", json={"question": "Can I return a sale item?"})
    assert response.status_code == 200
    assert response.json() == {
        "answer": "Sale items can be returned for store credit.",
        "sources": ["returns.txt, page 1", "returns.txt, page 2", "shipping.txt, page 1"],
    }


def test_the_model_is_sent_the_question_and_the_chunks_loaded_at_startup():
    fake = FakeAsyncClient()
    with TestClient(app_with(fake)) as client:
        client.post("/ask", json={"question": "Can I return a sale item?"})
    assert len(fake.messages.calls) == 1
    content = fake.messages.calls[0]["messages"][0]["content"]
    assert "Question: Can I return a sale item?" in content
    assert "Standard shipping takes five business days." in content


def test_a_body_without_a_question_is_refused_before_the_model_is_called():
    fake = FakeAsyncClient()
    with TestClient(app_with(fake)) as client:
        assert client.post("/ask", json={"q": "Can I return a sale item?"}).status_code == 422
    assert fake.messages.calls == []
