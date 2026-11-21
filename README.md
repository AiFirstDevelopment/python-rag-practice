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
| 9. Script to service | 47-49 | a FastAPI endpoint, an app you can test, a run report |
| 10. Capstone | 50 | a pipeline over new documents, from nothing, graded by its golden set |

Every model call in the tests goes to a fake, so the whole path runs offline and free.
