import importlib.util
import json
import sys
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

_spec = importlib.util.spec_from_file_location("solution_10", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = solution      # dataclasses and pydantic look a class's module up by name
_spec.loader.exec_module(solution)

GOOD = {"id": "returns-02", "question": "Can I get my money back for a sale item?", "expected_behavior": "answer",
        "required_facts": [{"fact": "store credit", "match": ["store credit"]},
                           {"fact": "within 14 days", "match": ["14 days", "fourteen days"]}],
        "sources": [{"file": "returns.txt", "page": 1}]}
FALLBACK = {"id": "absent-01", "question": "What are your store opening hours?", "expected_behavior": "fallback",
            "required_facts": [], "sources": []}


def line(**changes):
    return json.dumps({**GOOD, **changes})


def without(key):
    return json.dumps({k: v for k, v in GOOD.items() if k != key})


def test_a_good_line_becomes_a_case_with_typed_fields():
    case = solution.parse_case(json.dumps(GOOD))
    assert isinstance(case, solution.Case) and isinstance(case, BaseModel)
    assert case.id == "returns-02" and case.expected_behavior == "answer"
    assert isinstance(case.required_facts[1], solution.Fact)
    assert case.required_facts[1].match == ["14 days", "fourteen days"]
    assert isinstance(case.sources[0], solution.Source)
    assert (case.sources[0].file, case.sources[0].page) == ("returns.txt", 1)


def test_a_fallback_case_may_have_no_facts_and_no_sources():
    case = solution.parse_case(json.dumps(FALLBACK))
    assert case.expected_behavior == "fallback" and case.required_facts == [] and case.sources == []


def test_an_unknown_expected_behavior_is_rejected():
    with pytest.raises(ValidationError):
        solution.parse_case(line(expected_behavior="fallbak"))


def test_a_missing_field_is_rejected():
    for key in GOOD:
        with pytest.raises(ValidationError):
            solution.parse_case(without(key))


def test_an_empty_question_is_rejected():
    with pytest.raises(ValidationError):
        solution.parse_case(line(question=""))


def test_a_page_that_is_not_a_number_or_is_below_one_is_rejected():
    with pytest.raises(ValidationError):
        solution.parse_case(line(sources=[{"file": "returns.txt", "page": "one"}]))
    with pytest.raises(ValidationError):
        solution.parse_case(line(sources=[{"file": "returns.txt", "page": 0}]))


def test_a_line_that_is_not_json_raises_a_value_error():
    with pytest.raises(ValueError):
        solution.parse_case("not json")


def test_load_cases_keeps_good_cases_and_numbers_the_bad_lines():
    lines = [json.dumps(GOOD), "", "not json", json.dumps(FALLBACK), "   ", line(expected_behavior="maybe")]
    cases, bad = solution.load_cases(lines)
    assert [case.id for case in cases] == ["returns-02", "absent-01"]
    assert bad == [3, 6]
    assert solution.load_cases([]) == ([], [])
