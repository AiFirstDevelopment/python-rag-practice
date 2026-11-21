"""Grades the tests in solution.py: they must pass against implementations/correct and fail against every other
folder of implementations/, each of which has one bug. See "How it is graded" in the README."""
import ast
import functools
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


@functools.cache
def run_your_tests(implementation):
    """pytest on solution.py, in its own process, with implementations/<implementation> on the import path."""
    env = {**os.environ, "PYTHONPATH": str(HERE / "implementations" / implementation), "PYTHONDONTWRITEBYTECODE": "1"}
    command = [sys.executable, "-m", "pytest", str(HERE / "solution.py"), "-p", "no:cacheprovider", "--tb=short"]
    return subprocess.run(command, cwd=HERE, env=env, capture_output=True, text=True)


def pass_on_correct():
    run = run_your_tests("correct")
    assert run.returncode != 5, "solution.py has no tests yet: pytest found no function whose name starts with test_."
    assert run.returncode == 0, (
        "Your tests must all pass against implementations/correct. This is what pytest said:\n\n"
        + run.stdout[-3000:] + run.stderr[-1500:])


def caught(implementation, bug):
    pass_on_correct()
    survived = run_your_tests(implementation).returncode == 0
    assert not survived, (
        f"All your tests pass against implementations/{implementation}, {bug}. Add a test that fails on it.")


def decorated_tests(word):
    """The names of the test functions in solution.py that have a decorator with `word` in it."""
    tree = ast.parse((HERE / "solution.py").read_text(encoding="utf-8"))
    return [node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
            and any(word in ast.unparse(decorator) for decorator in node.decorator_list)]


def test_your_tests_pass_against_the_correct_implementation():
    pass_on_correct()


def test_at_least_one_of_your_tests_is_parametrized():
    pass_on_correct()
    assert decorated_tests("parametrize"), "No test in solution.py has @pytest.mark.parametrize above it."


def test_your_tests_catch_a_parse_score_that_refuses_one():
    caught("rejects_one", "which refuses a score of exactly 1")


def test_your_tests_catch_a_parse_score_that_refuses_zero():
    caught("rejects_zero", "which refuses a score of exactly 0")


def test_your_tests_catch_a_parse_score_that_accepts_more_than_one():
    caught("accepts_above_one", "which returns numbers above 1 instead of raising ValueError")


def test_your_tests_catch_a_parse_score_that_accepts_negative_numbers():
    caught("accepts_negative", "which returns numbers below 0 instead of raising ValueError")


def test_your_tests_catch_a_parse_score_that_returns_zero_for_text_that_is_not_a_number():
    caught("zero_for_text", "which returns 0.0 for text that is not a number instead of raising ValueError")
