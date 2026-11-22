# Python RAG Practice: plan

A Claude Code skill and a set of graded exercises that take a software engineer from no Python to building a RAG
pipeline and its eval harness by hand. It is the practice half of
[python-essentials-for-rag](https://github.com/AiFirstDevelopment/python-essentials-for-rag): the video course shows
the code; this repository makes you write it.

## How it works

- `/practice` in Claude Code (VS Code or the terminal) opens the next exercise: what to write, in a few lines, and a
  starter file with the function signatures.
- `/check` runs that exercise's tests (pytest). The tests decide pass or fail, never Claude's opinion.
- On a fail, the tutor leads instead of fixing: first a question about the failing test, then a hint, then the
  concept, and the solution only when you ask for it. It never edits your file.
- `progress.json` (not committed) records each exercise passed, the hints it took and the mistakes made; the next
  session picks up there, and an exercise you struggled with comes back later as a short review.
- Every test runs offline and free: model calls go to a scripted fake client, embeddings to a small fake. No API key
  is needed.

## Layout

```
.claude/skills/TUTOR.md            the tutor's rules: order, the hint ladder, never write the answer, progress
.claude/skills/practice/SKILL.md   /practice: opens the next exercise
.claude/skills/check/SKILL.md      /check: runs its tests and tutors a failure
exercises/NN-slug/README.md        the task
exercises/NN-slug/solution.py      your file (starts as the starter; 50 has none, you create pipeline.py)
exercises/NN-slug/test_*.py        the tests the tutor runs
exercises/17-20/implementations/   module 4: the correct and broken code your tests are graded against
exercises/50-capstone/corpus/      the capstone's documents, with its golden.jsonl
progress.json                      your record (gitignored)
pyproject.toml, uv.lock            Python 3.12, pytest, the same packages as the course
```

The tests sit beside your file, so you can read them; the README says reading them is fine (they are the spec), the
tutor asks you to try first.

## Curriculum (about 50 exercises, in order)

Each module matches a chapter of the course, so a viewer can watch the chapter and then do its exercises.

1. **Syntax and data** (ch. 2-3), 7: strings and f-strings; lists and slicing; dicts; loops and comprehensions;
   functions and default arguments; exceptions; counting words in a text.
2. **Types** (ch. 4), 4: type hints; dataclasses; pydantic models that validate a golden-set line; Optional and
   unions.
3. **Packages and files** (ch. 5-6), 5: a module of your own and imports; pathlib; reading and writing JSON and
   JSONL; reading a PDF's pages with pypdf; environment variables and a .env file.
4. **Testing** (ch. 9, moved forward so you test your own code from here on), 4: a first pytest; parametrize;
   fixtures; faking a dependency.
5. **NumPy and vectors** (ch. 7), 4: arrays; dot product and cosine similarity; top-k by similarity; a matrix of
   embeddings searched at once.
6. **Async and a model** (ch. 8), 5: a first model call and its token counts; system prompt and messages; parsing
   JSON the model returns, and refusing bad JSON; async and gather; retries with backoff.
7. **The pipeline** (ch. 10), 10: chunk text at sentence ends to about 900 characters; keep file and page with each
   chunk; BM25 keyword search; vector search; reciprocal rank fusion (k = 60); reranking with a model; widening a
   chunk with its neighbours; a prompt that answers from passages only; "I don't know" when nothing fits; the whole
   pipeline in one function.
8. **The eval harness** (ch. 11), 7: load the golden set; score retrieval (did it find the sources); check required
   facts in an answer; pass, fail and review; run cases concurrently; compare two runs and tell a gain from noise;
   fail CI on a real drop.
9. **From script to service** (ch. 12-13), 3: a FastAPI endpoint for the pipeline; testing it; a run report (the
   summary the course's notebook explores, as functions).
10. **Capstone**, 1: the pipeline over a new set of documents, with no starter code, graded by its golden set (a
    harness of your own is suggested, not graded).

## Is it worth building (2026-11-21)

Claude Code alone can set an exercise and review an answer, but not over weeks: no fixed path, grading by opinion,
an instinct to fix your code, and no memory. The skill adds the four. The value is in the exercises and their tests,
not the skill file: about 50 exercises, each a README, a starter and tests.

## Build order

1. The skill, the layout, `/practice` and `/check`, with module 1 (7 exercises). Joel works through it and says
   whether the hint ladder feels right.
2. The other modules (built: all 50 exercises are in `exercises/`).
3. The public repository (Joel creates it; a session cannot), a README with how to install, and a Short.
4. An MCP server over the pipeline as a worked example (`examples/mcp-server/`, FastMCP, 2026-11-22): tools,
   resources, prompts, transports, sign-in, confirmations, long jobs; tested through an in-memory client and HTTP.
