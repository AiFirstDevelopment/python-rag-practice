from fastapi.testclient import TestClient

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class FakePipeline:
    """Answers every question the same way and remembers what it was asked."""

    def __init__(self, error=None):
        self.error = error
        self.questions = []

    async def __call__(self, question):
        self.questions.append(question)
        if self.error:
            raise self.error
        return "You have 30 days from delivery.", ["returns.txt, page 1", "faq.txt, page 2"]


def test_health_answers_ok():
    client = TestClient(solution.create_app(FakePipeline()))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_the_answer_and_its_sources():
    client = TestClient(solution.create_app(FakePipeline()))
    response = client.post("/ask", json={"question": "How long do I have to return an item?"})
    assert response.status_code == 200
    assert response.json() == {
        "answer": "You have 30 days from delivery.",
        "sources": ["returns.txt, page 1", "faq.txt, page 2"],
    }


def test_the_pipeline_gets_the_question_without_whitespace_at_its_ends():
    pipeline = FakePipeline()
    client = TestClient(solution.create_app(pipeline))
    client.post("/ask", json={"question": "  Can I return shoes?\n"})
    assert pipeline.questions == ["Can I return shoes?"]


def test_a_body_without_a_question_is_refused():
    pipeline = FakePipeline()
    client = TestClient(solution.create_app(pipeline))
    assert client.post("/ask", json={"q": "Can I return shoes?"}).status_code == 422
    assert client.post("/ask", json={"question": ["Can I return shoes?"]}).status_code == 422
    assert pipeline.questions == []


def test_an_empty_question_is_refused_and_the_pipeline_is_not_called():
    pipeline = FakePipeline()
    client = TestClient(solution.create_app(pipeline))
    assert client.post("/ask", json={"question": ""}).status_code == 422
    assert client.post("/ask", json={"question": "  \n "}).status_code == 422
    assert pipeline.questions == []


def test_a_pipeline_that_is_down_answers_503():
    client = TestClient(solution.create_app(FakePipeline(error=solution.PipelineDown("no index"))))
    response = client.post("/ask", json={"question": "Can I return shoes?"})
    assert response.status_code == 503
    assert response.json() == {"detail": "The pipeline is not available."}


def test_each_app_uses_the_pipeline_it_was_given():
    first, second = FakePipeline(), FakePipeline()
    TestClient(solution.create_app(first)).post("/ask", json={"question": "One?"})
    TestClient(solution.create_app(second)).post("/ask", json={"question": "Two?"})
    assert first.questions == ["One?"]
    assert second.questions == ["Two?"]
