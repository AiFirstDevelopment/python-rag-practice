---
name: progress
description: Show the learner's progress map - one cell per exercise, a row per module, passed cells lit, the current one outlined, opened as a picture in a VS Code tab. Use when the learner types /progress, asks where they are, how far along they are, or to see their status or map.
---

# /progress

1. Run `python3 .claude/skills/progress/progress_map.py`. It reads `progress.json` and `exercises/` and writes
   `lessons/progress.svg` and `lessons/progress.md` (gitignored).
2. Open it: `"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" -r lessons/progress.md` (if not
   at that path, try `which code`). `.vscode/settings.json` opens `lessons/*.md` in the Markdown preview; if that
   setting is missing, add it back.
3. In the chat, one line: the count passed, the current exercise, and what is in `review`, if anything.

`/teach-me` and `/check` run step 1 after they change `progress.json`, so an open map tab stays current.
