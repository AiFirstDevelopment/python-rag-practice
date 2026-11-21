# 17. A first test

From here on you test your own code. A pipeline has a dozen small functions, and a change to one (a different chunk
size, a new cleaning rule) can quietly break another; the eval harness you build later is itself a test suite for
answers. A test is a function that calls your code and states what must be true with `assert`. `pytest` finds every
function whose name starts with `test_`, runs it, and reports the ones whose `assert` was false.

In this module the roles are swapped: the code is given, and you write the tests. Your tests go in `solution.py`.

## The code under test

A module `textkit` with the two functions of exercise 01:

- `clean(text)` returns the text with every run of whitespace (spaces, tabs, line breaks) turned into one space, and
  no whitespace at either end.
- `preview(text, n)` returns the first `n` characters of `text`; if the text was longer than `n`, it ends with `...`
  added after those `n` characters. A text of `n` characters or fewer comes back unchanged.

## What to write

In `solution.py`, replace the placeholder with test functions for `clean` and `preview`. Each test calls the function
and asserts the result, one behavior per test, with a name that says which:

```python
def test_clean_strips_the_ends():
    assert clean("  Hello world ") == "Hello world"
```

Keep the import at the top of the starter as it is.

## How it is graded

`implementations/` holds several versions of `textkit.py`: `correct/`, which does what is written above, and five
others, each with one bug. `/check` runs your tests once against each version (it starts pytest on `solution.py`
with that version's folder on the import path, so `from textkit import ...` gets that version):

- against `correct`, every one of your tests must pass, and there must be at least one;
- against each broken version, at least one of your tests must fail. A broken version that passes all your tests
  is a bug your tests would have let through.

When a check fails, its message says which version got past your tests and what that version gets wrong. Reading the
broken versions is allowed, but try first from the two descriptions above: ask of each sentence what a wrong
implementation would do, and write the test that would notice.

To run your tests yourself against the correct version, from the repository root:

```bash
PYTHONPATH=exercises/17-first-test/implementations/correct uv run pytest exercises/17-first-test/solution.py
```

You will use: `def test_...():`, `assert actual == expected`, one behavior per test.
