import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Case, Fact = solution.Case, solution.Fact

ANSWER = Case(
    id="returns-02", category="answerable", question="Can I get my money back for a sale item?",
    expected_behavior="answer",
    required_facts=[Fact(fact="store credit", match=["store credit"]),
                    Fact(fact="within 14 days", match=["14 days", "fourteen days"])],
    sources=[],
)
ABSENT = Case(id="absent-01", category="absent", question="What are your opening hours?",
              expected_behavior="fallback", required_facts=[], sources=[])


def test_fell_back_finds_a_fallback_phrase_in_any_case():
    assert solution.fell_back("I Do Not Know.") is True
    assert solution.fell_back("The policy doesn't say.") is True
    assert solution.fell_back("We open at nine.") is False


def test_a_fallback_case_that_says_it_does_not_know_passes():
    assert solution.score_answer(ABSENT, "I don't know.") == ("pass", [])


def test_a_fallback_case_that_was_answered_goes_to_review():
    assert solution.score_answer(ABSENT, "We open at nine every day.") == ("review", [])


def test_an_answer_with_every_fact_passes():
    assert solution.score_answer(ANSWER, "As store credit, within 14 days.") == ("pass", [])


def test_an_answer_missing_a_fact_fails_and_names_it():
    assert solution.score_answer(ANSWER, "You get store credit.") == ("fail", ["within 14 days"])


def test_a_right_answer_with_a_caveat_still_passes():
    reply = "Store credit, within 14 days. I don't know about opened items."
    assert solution.score_answer(ANSWER, reply) == ("pass", [])


def test_an_answer_case_that_fell_back_fails_with_every_fact_missing():
    assert solution.score_answer(ANSWER, "I don't know.") == ("fail", ["store credit", "within 14 days"])


def test_tally_always_has_the_three_statuses():
    assert solution.tally(["pass", "review", "pass"]) == {"pass": 2, "fail": 0, "review": 1}
    assert solution.tally([]) == {"pass": 0, "fail": 0, "review": 0}
