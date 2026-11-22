---
name: check
description: Grade the learner's current Python exercise with its tests, then tutor them through any failure without writing their code. Use when the learner types /check, says they are done with an exercise, or asks why their code fails.
---

# /check

Read `.claude/skills/TUTOR.md` (beside this skill's folder) first and follow it.

1. The exercise is `progress.json`'s `current`, or the one they name. If it has `"taught": true`, it was taught by
   `/teach-me`: score by `.claude/skills/teach-me/SKILL.md` steps 4-5 instead of the steps below.
2. Run its tests: `uv run pytest exercises/<NN-slug>`. If `uv` is missing, tell them to install it
   (`curl -LsSf https://astral.sh/uv/install.sh | sh`) and stop.
3. Read the test output and their files: `solution.py`; for 12 also `cleaning.py`; for 50 `pipeline.py` (there is no
   `solution.py`). In module 4 (17-20) `solution.py` holds their tests, and the grader's message names the broken
   implementation their tests let through.
4. All tests pass: follow TUTOR.md's "On a pass", record it in `progress.json`, and offer `/teach-me`.
5. A test fails: follow TUTOR.md's ladder, one rung, and record `checks`, `rungs` and the mistake in a few words.
   They have not started when the output shows the starter's `NotImplementedError`, `No module named 'cleaning'`
   (12) or "there is no pipeline.py" (50): say what to write first (in module 4, the first behavior to test), and
   take no rung.
6. Never edit the learner's files (TUTOR.md, "Never write their code").
