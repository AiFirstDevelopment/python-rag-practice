# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
# Your tests go in this file. Keep these imports: the grader decides which implementation of store it finds.
import json

import pytest

from store import append_jsonl, read_jsonl


# Your tests: replace this placeholder with tests for append_jsonl and read_jsonl. Every file they touch must be inside
# tmp_path. Define at least one fixture of your own with @pytest.fixture and use it in at least one test. Against the
# correct store every test must pass; against each of the four broken versions at least one must fail (a test that
# stops with an error counts as failing). Behaviors to cover:
#   append_jsonl(path, row) adds the dict row as one line of JSON at the end of the file, after whatever is already
#   there, and creates the file if it does not exist.
#   read_jsonl(path) returns the rows of the file as a list of dicts, in order:
#     lines that are empty or only whitespace are skipped;
#     the last line counts whether or not the file ends with a line break;
#     a file that does not exist gives [] (no results yet), not an error.
def test_replace_this_with_your_own_tests():
    raise NotImplementedError
