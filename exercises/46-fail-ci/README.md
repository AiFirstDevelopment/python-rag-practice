# 46. Fail CI on a real drop

A harness nobody runs protects nothing. In CI it runs on every pull request and compares the new run with the one
saved from the main branch. CI knows one thing about a step: its exit code, 0 for success and anything else for
failure. So the harness turns its verdict into an exit code: a real drop fails the build, noise and gains do not.

A run file is JSONL, one result a line: `{"id": "returns-01", "status": "pass"}`. The starter gives you `compare` and
`verdict` from exercise 45.

Write in `solution.py`:

- `load_run(path)`: the run file at `path` as a dict from id to status. Blank lines are skipped.
- `gate(before, after, threshold=2)`: compares the two runs (dicts) and returns a tuple `(code, message)`.
  - `code` is 1 when the verdict is `"drop"`, otherwise 0.
  - `message` is one line that contains the verdict word (`drop`, `gain` or `noise`). On a drop it also contains the
    id of every lost case. The rest of the wording is yours.
- `main(argv)`: `argv` is the list of command-line arguments without the program name: the path of the baseline run
  file, then the path of the new one. It prints the gate's message and returns the gate's code, with the default
  threshold.
  - If `argv` does not hold exactly two arguments, it prints a line containing the word `usage` and returns 2.
  - If either file does not exist, it prints a line containing that file's path and returns 2.

The last two lines of the starter call `main` when the file is run as a script, so this works:

```
$ uv run python exercises/46-fail-ci/solution.py main-run.jsonl new-run.jsonl
drop: 3 lost (returns-02, shipping-01, warranty-01), 0 gained
$ echo $?
1
```

You will use: `json.loads`, `Path.read_text`, a dict comprehension, returning a tuple, `print`,
`except FileNotFoundError`, `sys.exit`.
