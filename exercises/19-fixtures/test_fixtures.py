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


def tree():
    return ast.parse((HERE / "solution.py").read_text(encoding="utf-8"))


def fixtures():
    """The names of the functions in solution.py that have @pytest.fixture above them."""
    return [node.name for node in ast.walk(tree()) if isinstance(node, ast.FunctionDef)
            and any("fixture" in ast.unparse(decorator) for decorator in node.decorator_list)]


def parameters():
    """Every parameter name of every test and fixture in solution.py."""
    return {argument.arg for node in ast.walk(tree()) if isinstance(node, ast.FunctionDef)
            for argument in node.args.args}


def test_your_tests_pass_against_the_correct_implementation():
    pass_on_correct()


def test_you_wrote_a_fixture_and_a_test_uses_it():
    pass_on_correct()
    assert fixtures(), "solution.py defines no fixture: no function has @pytest.fixture above it."
    assert set(fixtures()) & parameters(), (
        f"No test asks for your fixture. Name it as a parameter: def test_something({fixtures()[0]}): ...")
    assert "tmp_path" in parameters(), "Nothing in solution.py asks for tmp_path; test files belong in it."


def test_your_tests_catch_an_append_that_replaces_the_file():
    caught("overwrites", "whose append_jsonl replaces what was in the file instead of adding a line after it")


def test_your_tests_catch_a_read_that_fails_on_blank_lines():
    caught("blank_lines_crash", "whose read_jsonl raises an error on a file with a blank line in it")


def test_your_tests_catch_a_read_that_fails_on_a_missing_file():
    caught("missing_file_raises", "whose read_jsonl raises an error instead of returning [] for a file that does not exist")


def test_your_tests_catch_a_read_that_loses_a_last_line_without_a_line_break():
    caught("drops_unterminated_last_line",
           "whose read_jsonl loses the last row when the file does not end with a line break")
