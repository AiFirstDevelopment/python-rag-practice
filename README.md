# Python RAG Practice

Graded Python exercises, with a tutor in Claude Code, from no Python to building a RAG pipeline and its eval harness
by hand. The practice half of [python-essentials-for-rag](https://github.com/AiFirstDevelopment/python-essentials-for-rag):
the course shows the code, this makes you write it.

Ready to be tested? [The Python readiness check](https://joelstevick.com/learn/python-assessment): a timed Python
coding test Claude writes for your level, scored by hidden tests.

## Start

Make your own copy first, so your solutions are yours to commit and push: press **Use this template** on GitHub
(or fork it), then clone your copy. This repo's `main` takes changes only by pull request; it is the course, not a
place for your answers.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv, if you don't have it
uv sync
claude                                            # or open the folder in VS Code with Claude Code
```

Then in Claude Code:

- `/teach-me` opens the next exercise and teaches it from a worked example: a lesson opens in a VS Code tab, you
  close it and write the code from memory.
- `/check` runs its tests, scores your attempt, shows each mistake and the line that caused it, and offers a restart
  from a blank file until it passes. It never edits your code.
- `/progress` shows your map: one cell per exercise, a row per module, the passed ones lit.

In each starter file, search for `EXERCISE-TODO`: every piece you write has one, with its requirements.
Each exercise's task is in its folder's `README.md` (the first line of its starter file says so), and
`/progress` links to the current one. Your progress is kept in `progress.json` (not committed). Everything runs offline; no API key is needed.

The tests sit next to your file. Reading them is allowed (they are the spec), but try first. Later exercises give
you earlier ones' code as starting points, so don't open exercises ahead of the one you're on.

## The path

Fifty exercises, each matched to a chapter of the course:

| Module | Exercises | What you write |
|---|---|---|
| 1. Syntax and data | 01-07 | strings, lists, dictionaries, comprehensions, functions, exceptions, a word count |
| 2. Types | 08-11 | type hints, dataclasses, a pydantic model for a golden-set line, Optional and unions |
| 3. Packages and files | 12-16 | your own module, pathlib, JSON and JSONL, a PDF's pages, a `.env` file |
| 4. Testing | 17-20 | your own tests, graded against a correct version and several broken ones |
| 5. NumPy and vectors | 21-24 | arrays, cosine similarity, top-k, a matrix of embeddings searched at once |
| 6. Async and a model | 25-29 | a model call and its cost, messages, JSON from a model, gather with a limit, retries |
| 7. The pipeline | 30-39 | chunking, BM25, vector search, rank fusion, reranking, widening, the prompt, "I don't know", the whole pipeline |
| 8. The eval harness | 40-46 | the golden set, retrieval recall, required facts, pass / fail / review, concurrent runs, gain or noise, a CI gate |
| 9. A FastAPI service | 47-49 | a FastAPI endpoint, an app you can test, a run report |
| 10. Final project | 50 | a pipeline over new documents, from nothing, graded by its golden set |

Every model call in the tests goes to a fake, so the whole path runs offline and free.

## An MCP server for the pipeline

[`examples/mcp-server/`](examples/mcp-server/) is a complete MCP server, built with FastMCP, that makes the final project's
documents and a live booking system available to Claude Code: tools, resources and prompts, stdio and HTTP, sign-in
and per-user access, confirmations, long jobs, paging and an audit log, every part commented with why it is built
that way. Add it to Claude Code with one line (its README) and try it, or read it after the final project.
