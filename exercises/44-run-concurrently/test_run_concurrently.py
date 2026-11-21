import asyncio

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Case, Fact, Result = solution.Case, solution.Fact, solution.Result


def answer_case(n):
    return Case(id=f"case-{n}", category="answerable", question=f"question {n}", expected_behavior="answer",
                required_facts=[Fact(fact="30 days", match=["30 days"])], sources=[])


ABSENT = Case(id="absent-01", category="absent", question="opening hours?", expected_behavior="fallback",
              required_facts=[], sources=[])


class FakePipeline:
    """Replies after a short wait and records how many calls were in flight at once."""

    def __init__(self, replies=None, waits=None, crash_on=()):
        self.replies, self.waits, self.crash_on = replies or {}, waits or {}, crash_on
        self.questions, self.in_flight, self.peak = [], 0, 0

    async def __call__(self, question):
        self.questions.append(question)
        self.in_flight += 1
        self.peak = max(self.peak, self.in_flight)
        try:
            await asyncio.sleep(self.waits.get(question, 0.01))
            if question in self.crash_on:
                raise RuntimeError(f"boom on {question}")
            return self.replies.get(question, "Within 30 days.")
        finally:
            self.in_flight -= 1


def test_results_are_in_case_order_even_when_later_cases_finish_first():
    cases = [answer_case(n) for n in range(4)]
    pipeline = FakePipeline(waits={"question 0": 0.05, "question 1": 0.03})
    results = asyncio.run(solution.run_cases(cases, pipeline, limit=4))
    assert [r.id for r in results] == ["case-0", "case-1", "case-2", "case-3"]


def test_each_reply_is_scored():
    cases = [answer_case(0), answer_case(1), ABSENT]
    pipeline = FakePipeline(replies={"question 1": "Within a month.", "opening hours?": "We open at nine."})
    results = asyncio.run(solution.run_cases(cases, pipeline, limit=3))
    assert results == [
        Result("case-0", "pass", [], None),
        Result("case-1", "fail", ["30 days"], None),
        Result("absent-01", "review", [], None),
    ]


def test_the_pipeline_is_called_once_per_case_with_its_question():
    cases = [answer_case(n) for n in range(5)]
    pipeline = FakePipeline()
    asyncio.run(solution.run_cases(cases, pipeline, limit=2))
    assert sorted(pipeline.questions) == [f"question {n}" for n in range(5)]


def test_up_to_the_limit_run_at_once_and_never_more():
    pipeline = FakePipeline()
    asyncio.run(solution.run_cases([answer_case(n) for n in range(7)], pipeline, limit=3))
    assert pipeline.peak == 3


def test_a_limit_of_one_runs_them_one_at_a_time():
    pipeline = FakePipeline()
    asyncio.run(solution.run_cases([answer_case(n) for n in range(4)], pipeline, limit=1))
    assert pipeline.peak == 1


def test_a_case_whose_pipeline_raises_fails_and_the_rest_still_run():
    cases = [answer_case(0), answer_case(1), answer_case(2)]
    pipeline = FakePipeline(crash_on={"question 1"})
    results = asyncio.run(solution.run_cases(cases, pipeline, limit=2))
    assert [r.status for r in results] == ["pass", "fail", "pass"]
    assert results[1].missing == []
    assert results[1].error == "boom on question 1"
    assert results[0].error is None


def test_no_cases_is_an_empty_list():
    assert asyncio.run(solution.run_cases([], FakePipeline(), limit=4)) == []
