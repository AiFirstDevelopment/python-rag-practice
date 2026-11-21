---
name: check
description: Grade the learner's current Python exercise with its tests, then tutor them through any failure without writing their code. Use when the learner types /check, says they are done with an exercise, or asks why their code fails.
---

# /check

Read `../TUTOR.md` first and follow it.

1. The exercise is `progress.json`'s `current`, or the one they name.
2. Run its tests: `uv run pytest exercises/<NN-slug>`. If `uv` is missing, tell them to install it
   (`curl -LsSf https://astral.sh/uv/install.sh | sh`) and stop.
3. Read their `solution.py` and the test output.
4. All tests pass: follow TUTOR.md's "On a pass", record it in `progress.json`, and offer `/practice`.
5. A test fails: follow TUTOR.md's ladder, one rung, and record `checks`, `rungs` and the mistake in a few words.
   A `NotImplementedError` means they have not started: say which function to write first.
6. Never edit `solution.py`.
