import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Fact = solution.Fact

CREDIT = Fact(fact="store credit", match=["store credit"])
DAYS = Fact(fact="within 14 days", match=["14 days", "fourteen days"])
PHOTO = Fact(fact="attach a photo", match=["photo"])


def test_a_match_string_in_the_answer_is_the_fact():
    assert solution.has_fact(CREDIT, "Sale items are refunded as store credit.") is True
    assert solution.has_fact(CREDIT, "Sale items are refunded in cash.") is False


def test_any_one_of_the_match_strings_is_enough():
    assert solution.has_fact(DAYS, "You have fourteen days.") is True
    assert solution.has_fact(DAYS, "You have 14 days.") is True


def test_case_of_the_answer_does_not_matter():
    assert solution.has_fact(DAYS, "Within FOURTEEN DAYS of delivery.") is True


def test_case_of_the_match_string_does_not_matter():
    assert solution.has_fact(Fact(fact="not matched", match=["No."]), "no. marketplace sellers are excluded") is True


def test_it_is_a_substring_search():
    assert solution.has_fact(Fact(fact="tennis balls", match=["tennis ball"]), "Add two tennis balls.") is True


def test_a_fact_with_no_match_strings_is_never_found():
    assert solution.has_fact(Fact(fact="anything", match=[]), "anything") is False


def test_missing_facts_are_named_in_the_order_given():
    assert solution.missing_facts([DAYS, CREDIT, PHOTO], "You get store credit.") == ["within 14 days", "attach a photo"]


def test_nothing_missing_is_an_empty_list():
    assert solution.missing_facts([CREDIT, DAYS], "Store credit, within 14 days.") == []
    assert solution.missing_facts([], "anything") == []
