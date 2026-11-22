---
name: reset-all-exercises
description: Wipe all of the learner's work so they can start the course fresh - every solution file back to its starter, files they created in exercises/ deleted, progress.json and lessons/ deleted - only after they confirm. Use when the learner types /reset-all-exercises or asks to reset everything, wipe their progress, or start the whole course over.
---

# /reset-all-exercises

This destroys the learner's work and cannot be undone by the tutor. Never run it without their confirmation in this
turn's exchange; approval for an earlier reset does not carry over.

## 1. List what will go

Run these and show the result, grouped and short (counts, plus the file names when there are few):

- `git status --porcelain -- exercises/` : tracked starter files they changed (`M`, back to the starter) and files
  they created (`??`, deleted, e.g. `cleaning.py` in 12, `pipeline.py` in 50).
- `git clean -nd -- exercises/` : the untracked files that will be deleted.
- `progress.json` and `lessons/`, if they exist (deleted).

If nothing is listed, say there is nothing to reset and stop.

Committed work is not touched: if `git log origin/main..HEAD -- exercises/` shows commits of theirs, say that the reset
covers only uncommitted changes and those commits stay.

## 2. Confirm

Ask: "This permanently deletes all of the above. Type `yes` to reset everything." Proceed only on an explicit yes;
anything else cancels and changes nothing.

## 3. Reset

On yes, from the repository root:

```sh
git checkout -- exercises/
git clean -fd -- exercises/
rm -rf progress.json lessons/
```

Never touch anything outside `exercises/`, `progress.json` and `lessons/` (not `implementations/` beyond what
`git checkout` restores, not test files, not `.claude/`).

## 4. Hand over

One line: everything is reset, and `/teach-me` starts exercise 01.
