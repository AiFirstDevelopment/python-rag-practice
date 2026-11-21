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
    env = {**os.environ, "ANTHROPIC_API_KEY": "", "PYTHONPATH": str(HERE / "implementations" / implementation), "PYTHONDONTWRITEBYTECODE": "1"}
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


def parameters():
    """Every parameter name of every test and fixture in solution.py."""
    tree = ast.parse((HERE / "solution.py").read_text(encoding="utf-8"))
    return {argument.arg for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
            for argument in node.args.args}


def test_your_tests_pass_against_the_correct_implementation():
    pass_on_correct()


def test_a_test_uses_monkeypatch_for_the_environment_variable():
    pass_on_correct()
    assert "monkeypatch" in parameters(), (
        "No test asks for monkeypatch. Set PRACTICE_MODEL with monkeypatch.setenv so the change ends with the test.")


def test_your_tests_catch_an_ask_that_calls_the_model_with_no_passages():
    caught("calls_without_passages", "whose ask calls the model even when there are no passages")


def test_your_tests_catch_an_ask_that_sends_only_the_first_passage():
    caught("first_passage_only", "whose ask puts only the first passage in the message")


def test_your_tests_catch_an_ask_that_leaves_the_question_out():
    caught("drops_question", "whose ask sends the passages without the question")


def test_your_tests_catch_an_ask_that_swaps_the_token_counts():
    caught("swaps_token_counts", "whose ask returns the output tokens as input_tokens and the input tokens as output_tokens")


def test_your_tests_catch_an_ask_that_ignores_the_model_variable():
    caught("ignores_model_variable", "whose ask always uses DEFAULT_MODEL and never reads PRACTICE_MODEL")
