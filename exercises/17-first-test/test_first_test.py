"""Grades the tests in solution.py: they must pass against implementations/correct and fail against every other
folder of implementations/, each of which has one bug. See "How it is graded" in the README."""
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


def test_your_tests_pass_against_the_correct_implementation():
    pass_on_correct()


def test_your_tests_catch_a_clean_that_keeps_whitespace_at_the_ends():
    caught("keeps_ends", "whose clean leaves a space at either end of the text")


def test_your_tests_catch_a_clean_that_only_collapses_spaces():
    caught("spaces_only", "whose clean collapses runs of spaces but leaves tabs and line breaks inside the text")


def test_your_tests_catch_a_preview_that_marks_a_text_of_exactly_n_characters():
    caught("marks_exact_length", "whose preview adds ... to a text that is exactly n characters long")


def test_your_tests_catch_a_preview_that_never_adds_the_marker():
    caught("never_marks", "whose preview cuts a long text but never adds ...")


def test_your_tests_catch_a_preview_that_counts_the_marker_in_n():
    caught("counts_marker", "whose preview keeps only n - 3 characters of a long text before the ...")
