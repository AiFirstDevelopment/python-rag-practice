# 19. Fixtures

Code that reads and writes files needs files to test with, and a test must never leave them behind or depend on what
another test wrote. A fixture is a function that prepares what a test needs; a test asks for it by naming it as a
parameter, and pytest runs the fixture first and passes in what it returned. `tmp_path` is a fixture pytest already
has: a new empty folder (a `Path`) for each test, cleaned up later.

As in exercises 17 and 18, the code is given and you write its tests in `solution.py`.

## The code under test

A module `store` with two functions of exercise 14, as the eval harness uses them to keep each case's result:

- `append_jsonl(path, row)` adds the dict `row` as one line of JSON at the end of the file at `path`, after
  whatever is already there, and creates the file if it does not exist.
- `read_jsonl(path)` returns the rows of the file as a list of dicts, in order.
  - Lines that are empty or only whitespace are skipped.
  - The last line counts whether or not the file ends with a line break.
  - A file that does not exist gives `[]` (no results yet), not an error.

## What to write

In `solution.py`, replace the placeholder with tests for the two functions. Every file your tests touch must be
inside `tmp_path`. Write at least one fixture of your own and use it in at least one test: for example one that
writes a small results file into `tmp_path` and returns its path, so that several tests start from the same file
without repeating the lines that make it.

```python
@pytest.fixture
def notes_file(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("first\nsecond\n", encoding="utf-8")
    return path


def test_notes_has_two_lines(notes_file):
    assert len(notes_file.read_text(encoding="utf-8").splitlines()) == 2
```

A fixture can ask for another fixture the same way a test does, as `notes_file` asks for `tmp_path`. To test how
`read_jsonl` treats a file in a particular state (blank lines, no line break at the end), write that file's text
yourself with `path.write_text(...)`.

Keep the imports at the top of the starter as they are.

## How it is graded

The same way as exercise 17. `implementations/` holds a correct `store.py` and four with one bug each; `/check`
runs your tests against each. They must all pass against `correct` and at least one must fail against each of the
others (a test that stops with an error, because the broken version raised one, counts as failing). It also checks
that `solution.py` defines a fixture with `@pytest.fixture` and that a test uses it.

To run your tests yourself against the correct version, from the repository root:

```bash
PYTHONPATH=exercises/19-fixtures/implementations/correct uv run pytest exercises/19-fixtures/solution.py
```

You will use: `tmp_path`, `@pytest.fixture`, a fixture's name as a test's parameter, `path.write_text`,
`path.exists()`.
