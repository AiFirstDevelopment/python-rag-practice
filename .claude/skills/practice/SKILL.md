---
name: practice
description: Open the next Python exercise in this repository - the graded path from no Python to a RAG pipeline and its eval harness. Use when the learner types /practice, asks for the next exercise, or asks where they are.
---

# /practice

Read `.claude/skills/TUTOR.md` (beside this skill's folder) first and follow it.

1. Read `progress.json` (create it with `{"current": null, "exercises": {}, "review": []}` if missing).
2. Pick the exercise by TUTOR.md's "Order". If one is `started` and not passed, it is still the current one: say so
   and repeat its task.
3. Show the task from its `README.md` in a few lines: what to write, one example, and the file to edit, as a
   clickable path: `exercises/NN-slug/solution.py`; for 12 also `cleaning.py`, which they create; for 50
   `pipeline.py`, which they create (there is no starter). In module 4 (17-20) say that they write tests, not the
   code. Do not paste the tests.
4. Set `current` and mark it `started` in `progress.json`.
5. End with: "Write it, then type /check."

If every exercise is passed, say the path is complete, and offer the `review` list, if any is left, as practice.
If they ask where they are, give the count passed, the current exercise and what is in `review`.
