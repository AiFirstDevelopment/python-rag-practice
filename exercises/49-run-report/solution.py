# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
import json
from pathlib import Path


# EXERCISE-TODO: load_results(path): read the JSONL file at path (a pathlib.Path) and return a list of dicts, one per
# line, in file order. Blank lines are skipped.
def load_results(path: Path) -> list[dict]:
    raise NotImplementedError


# EXERCISE-TODO: summarize(results, input_price, output_price, slowest=3): return a dict with exactly these keys:
# "cases" (the number of results), "passed" (how many have status "pass"; only "pass" counts), "pass_rate" (passed /
# cases, a float from 0 to 1, 0.0 when there are no cases), "by_category" (each category to {"cases": ..., "passed":
# ..., "pass_rate": ...} for its results), "slowest" (the ids of the `slowest` cases with the most seconds, slowest
# first, all of them if fewer) and "cost" (the dollars for all the run's tokens; prices are dollars per million tokens).
#   summarize(first_four_results, 5.0, 25.0, slowest=2)
#     ->  {"cases": 4, "passed": 3, "pass_rate": 0.75, "by_category": {"answerable": {"cases": 3, "passed": 2,
#          "pass_rate": 0.666...}, "absent": {"cases": 1, "passed": 1, "pass_rate": 1.0}},
#          "slowest": ["returns-03", "returns-01"], "cost": 0.02875}
def summarize(results: list[dict], input_price: float, output_price: float, slowest: int = 3) -> dict:
    raise NotImplementedError


# EXERCISE-TODO: to_markdown(summary): return the summary as a Markdown table, lines joined with "\n": the header
# "| category | cases | passed | pass rate |", the separator "| --- | --- | --- | --- |", one row per category in
# alphabetical order, and a last row "all". Pass rates are whole percents (f"{rate:.0%}").
#   a row  ->  "| answerable | 3 | 2 | 67% |"
#   last   ->  "| all | 4 | 3 | 75% |"
def to_markdown(summary: dict) -> str:
    raise NotImplementedError
