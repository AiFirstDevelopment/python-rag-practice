# 18. Parametrize

Most tests of a pipeline are the same check over a table of inputs: this text gives this score, that one is refused.
Ten copies of one test function hide the table; one test with the table above it shows it, and pytest still reports
each row as its own test, so a failure names the row.

As in exercise 17, the code is given and you write its tests in `solution.py`.

## The code under test

A module `scores` with the first function of exercise 06, which reads the score a reranking model gave a passage:

- `parse_score(text)` returns the number in `text` as a float. Spaces around the number are allowed.
- It raises `ValueError` when the text is not a number.
- It raises `ValueError` when the number is outside 0 to 1. Both ends are allowed: `"0"` gives `0.0` and `"1"`
  gives `1.0`.

## What to write

In `solution.py`, replace the placeholder with tests for `parse_score`. At least one test must be parametrized: a
table of cases passed to one test function.

```python
@pytest.mark.parametrize("text, expected", [
    ("3", 3),
    (" 12 ", 12),
])
def test_int_reads_whole_numbers(text, expected):
    assert int(text) == expected
```

The first argument names the test function's parameters; the list holds one tuple per case. A natural split here is
one parametrized test for texts that give a score and one for texts that must be refused:

```python
def test_int_refuses_words():
    with pytest.raises(ValueError):
        int("three")
```

`pytest.raises` passes when the block raises that error and fails when it does not.

Keep the imports at the top of the starter as they are.

## How it is graded

The same way as exercise 17. `implementations/` holds a correct `scores.py` and five with one bug each; `/check`
runs your tests against each. They must all pass against `correct` and at least one must fail against each of the
others. It also checks that at least one of your tests uses `@pytest.mark.parametrize`.

To run your tests yourself against the correct version, from the repository root:

```bash
PYTHONPATH=exercises/18-parametrize/implementations/correct uv run pytest exercises/18-parametrize/solution.py
```

You will use: `@pytest.mark.parametrize("names", [cases])`, `with pytest.raises(ValueError):`, the edges of a range
as test cases.
