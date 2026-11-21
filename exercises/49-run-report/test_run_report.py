import json

import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

RESULTS = [
    {"id": "returns-01", "category": "answerable", "status": "pass", "seconds": 1.8,
     "input_tokens": 1200, "output_tokens": 80},
    {"id": "returns-02", "category": "answerable", "status": "fail", "seconds": 1.1,
     "input_tokens": 1100, "output_tokens": 60},
    {"id": "returns-03", "category": "answerable", "status": "pass", "seconds": 2.6,
     "input_tokens": 1300, "output_tokens": 90},
    {"id": "absent-01", "category": "absent", "status": "pass", "seconds": 0.9,
     "input_tokens": 900, "output_tokens": 20},
    {"id": "absent-02", "category": "absent", "status": "review", "seconds": 1.4,
     "input_tokens": 1000, "output_tokens": 50},
    {"id": "inferred-01", "category": "inferred", "status": "fail", "seconds": 3.2,
     "input_tokens": 1500, "output_tokens": 200},
]


def test_load_results_reads_one_dict_per_line_and_skips_blank_lines(tmp_path):
    path = tmp_path / "run.jsonl"
    lines = [json.dumps(result) for result in RESULTS]
    path.write_text(lines[0] + "\n\n" + "\n".join(lines[1:]) + "\n   \n", encoding="utf-8")
    assert solution.load_results(path) == RESULTS


def test_overall_counts_and_pass_rate_only_pass_counts():
    summary = solution.summarize(RESULTS, 5.0, 25.0)
    assert set(summary) == {"cases", "passed", "pass_rate", "by_category", "slowest", "cost"}
    assert summary["cases"] == 6
    assert summary["passed"] == 3
    assert summary["pass_rate"] == pytest.approx(0.5)


def test_counts_and_pass_rate_by_category():
    by_category = solution.summarize(RESULTS, 5.0, 25.0)["by_category"]
    assert set(by_category) == {"answerable", "absent", "inferred"}
    assert by_category["answerable"]["cases"] == 3
    assert by_category["answerable"]["passed"] == 2
    assert by_category["answerable"]["pass_rate"] == pytest.approx(2 / 3)
    assert by_category["absent"] == {"cases": 2, "passed": 1, "pass_rate": pytest.approx(0.5)}
    assert by_category["inferred"] == {"cases": 1, "passed": 0, "pass_rate": pytest.approx(0.0)}


def test_slowest_cases_slowest_first():
    assert solution.summarize(RESULTS, 5.0, 25.0)["slowest"] == ["inferred-01", "returns-03", "returns-01"]
    assert solution.summarize(RESULTS, 5.0, 25.0, slowest=1)["slowest"] == ["inferred-01"]
    assert len(solution.summarize(RESULTS[:2], 5.0, 25.0, slowest=5)["slowest"]) == 2


def test_cost_of_the_whole_run_at_prices_per_million_tokens():
    # 7,000 input tokens and 500 output tokens
    assert solution.summarize(RESULTS, 5.0, 25.0)["cost"] == pytest.approx(0.0475)
    assert solution.summarize(RESULTS, 1.0, 0.0)["cost"] == pytest.approx(0.007)


def test_a_run_of_no_cases():
    summary = solution.summarize([], 5.0, 25.0)
    assert summary == {"cases": 0, "passed": 0, "pass_rate": 0.0, "by_category": {}, "slowest": [], "cost": 0.0}


def test_markdown_table_has_a_row_per_category_in_alphabetical_order_then_all():
    table = solution.to_markdown(solution.summarize(RESULTS, 5.0, 25.0))
    assert table.strip().split("\n") == [
        "| category | cases | passed | pass rate |",
        "| --- | --- | --- | --- |",
        "| absent | 2 | 1 | 50% |",
        "| answerable | 3 | 2 | 67% |",
        "| inferred | 1 | 0 | 0% |",
        "| all | 6 | 3 | 50% |",
    ]


def test_markdown_table_of_no_cases_is_the_header_and_the_all_row():
    table = solution.to_markdown(solution.summarize([], 5.0, 25.0))
    assert table.strip().split("\n") == [
        "| category | cases | passed | pass rate |",
        "| --- | --- | --- | --- |",
        "| all | 0 | 0 | 0% |",
    ]
