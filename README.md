# Python RAG Practice

Graded Python exercises, with a tutor in Claude Code, from no Python to building a RAG pipeline and its eval harness
by hand. The practice half of [python-essentials-for-rag](https://github.com/AiFirstDevelopment/python-essentials-for-rag):
the course shows the code, this makes you write it.

## Start

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv, if you don't have it
uv sync
claude                                            # or open the folder in VS Code with Claude Code
```

Then in Claude Code:

- `/practice` opens the next exercise.
- `/check` runs its tests. When one fails, the tutor asks a question, then gives a hint, then explains the concept;
  it shows a solution only if you ask, and it never edits your file.

Your progress is kept in `progress.json` (not committed). Everything runs offline; no API key is needed.

The tests sit next to your file. Reading them is allowed (they are the spec), but try first.

## What's here

Module 1, syntax and data: strings, lists, dictionaries, comprehensions, functions, exceptions, and a word count.
The full path is in [PLAN.md](PLAN.md).
