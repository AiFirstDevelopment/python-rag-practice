# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
# Your tests go in this file. Keep these imports: the grader decides which implementation of scores it finds.
import pytest

from scores import parse_score


# Your tests: replace this placeholder with tests for parse_score. At least one test must use
# @pytest.mark.parametrize (a table of cases passed to one test function). Against the correct scores every test must
# pass; against each of the five broken versions at least one must fail. Behaviors to cover:
#   parse_score(text) returns the number in text as a float; spaces around the number are allowed.
#   It raises ValueError when the text is not a number (check with `with pytest.raises(ValueError):`).
#   It raises ValueError when the number is outside 0 to 1. Both ends are allowed:
#     parse_score("0")  ->  0.0
#     parse_score("1")  ->  1.0
def test_replace_this_with_your_own_tests():
    raise NotImplementedError
