---
name: practice
description: Open the next Python exercise in this repository - the graded path from no Python to a RAG pipeline and its eval harness. Use when the learner types /practice, asks for the next exercise, or asks where they are.
---

# /practice

Read `../TUTOR.md` first and follow it.

1. Read `progress.json` (create it with `{"current": null, "exercises": {}, "review": []}` if missing).
2. Pick the exercise by TUTOR.md's "Order". If one is `started` and not passed, it is still the current one: say so
   and repeat its task.
3. Show the task from its `README.md` in a few lines: what to write, one example, and the file to edit
   (`exercises/NN-slug/solution.py`, as a clickable path). Do not paste the tests.
4. Set `current` and mark it `started` in `progress.json`.
5. End with: "Write it, then type /check."

If every exercise is passed, say which module comes next in `PLAN.md` and that it is not built yet.
If they ask where they are, give the count passed, the current exercise and what is in `review`.
