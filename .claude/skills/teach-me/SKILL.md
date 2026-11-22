---
name: teach-me
description: Teach the learner's current Python exercise by worked example - a rendered lesson in a VS Code tab with the solution's key parts explained, then they write it from scratch, get scored, and may restart until it is clean. Use when the learner types /teach-me, asks to be taught or shown an exercise first, or says they don't know where to start.
---

# /teach-me

Read `.claude/skills/TUTOR.md` (beside this skill's folder) first. Its voice, progress and order rules apply; its
"Never write their code" rule is relaxed only as this skill says.

## 1. Pick the exercise

The one they name; else `progress.json`'s `current` if it is started and not passed (say so: it is still the one
they are on); else the next by TUTOR.md's "Order", which after every third pass puts a `review` exercise first: ask
them to solve one of its tests again from memory in the chat, with no lesson, then drop it from `review` and go on
to the next exercise. Set `current`, mark it `started`, and set `"taught": true` on it. If every exercise is passed,
go to the MCP server below.

### After the last exercise (54): the full MCP server

`examples/mcp-server/` is the full server that module 11 (51-54) builds toward: a worked example, not an
exercise. When every exercise is passed and `progress.json`'s
`"examples"` does not mark `"mcp-server"` done, set `current` to `"mcp-server"` and open its `README.md` in the
preview (`code -r examples/mcp-server/README.md`, then tell them to press Cmd+Shift+V if it shows the source). Walk
them through adding it to Claude Code and asking it one question from the README; once a tool call from it has
answered, set `"examples": {"mcp-server": "done"}` and run the progress map. Then say the path is complete and offer
what is left in `review` as practice.

## 2. Build the lesson page

Read the exercise's `README.md` and its tests. Write a worked solution yourself and verify it passes the tests
(in the scratchpad, never in their file). Then write the lesson to `lessons/NN-slug.md` (gitignored, never inside
`exercises/`) and open only the lesson (it carries the task): `"/Applications/Visual Studio
Code.app/Contents/Resources/app/bin/code" -r lessons/NN-slug.md` (if not at that path, try `which code`). `.vscode/settings.json` maps `**/lessons/*.md` to
VS Code's built-in Markdown preview, so the tab shows only the rendered lesson, never the source. If that setting is
missing, add it back.

The lesson (Markdown; see `lessons/01-strings.md` if it exists for the shape):

- `# ` the exercise name, then `## The task`: the README's task and examples (not the "You will use" line), and a
  link to it: `[The task, any time: exercises/NN-slug/README.md](../exercises/NN-slug/README.md)`.
- The file it belongs in, in bold (`solution.py`; `cleaning.py` for 12; `pipeline.py` for 50; in module 4, 17-20,
  the example is *tests*, not code).
- The full worked solution in a plain fenced ` ```python ` block. No highlights. Each line that carries a lesson
  ends with a comment holding circled numbers, in order: `  # ①`, or `  # ④ ⑤` for two on one line. Three to six
  numbers in all.
- Under the code, one note per number, headed by the number in bold and the bit of code it is about
  (`` **①** `text.split()`: ``): what it does and the Python idea behind it, two or three sentences. Plain
  engineer-to-engineer voice.
- A rule, then: "**Close this page and write it from memory: [open your solution.py](../exercises/NN-slug/solution.py)**
  (blank, or your last draft if you started). When you are done, save it and type `/check` in the Claude chat." Link
  the file they write (`cleaning.py` for 12, `pipeline.py` for 50; create an empty one first if it does not exist, so
  the link opens).

## 3. Hand over

The open lesson tab is the hand-over: say nothing about it in the chat, ask nothing, and do not paste the solution.
If they were on `main`, create and switch to a local `practice` branch before opening the lesson (their work stays
off `main`) and say only: "Created the practice branch."

If they come back to an exercise already `taught` and not passed, `/teach-me` teaches it again: reopen its lesson (rebuild it if `lessons/NN-slug.md` is missing; it starts with the task) and hand over as above.

## 4. Score their attempt

When they say they're done (or type /check), run `uv run pytest exercises/NN-slug` and read their file. Report:

- Score: tests passed out of total.
- Where it went wrong: for each failing test, the input, what was expected, what came back, and the line in their
  file that causes it (as a clickable path with line number). Name the cause plainly; since they have seen the
  solution, you may point to the lesson's note on that part ("see the note on `text.split()`").
- If all pass, say "passed", and at most one idiom note per TUTOR.md's "On a pass".

Record `checks` and the mistakes in `progress.json` silently (TUTOR.md, "Progress"). Do not edit their file to fix it.

## 5. Restart, only when they ask

Do not offer or ask about a restart; end the report with the failure, and they fix it or ask. If they ask to restart
the exercise from scratch, and only then:

- reset their file to the starter with `git checkout -- exercises/NN-slug/solution.py` (for 12, also delete
  `cleaning.py`; for 50, delete `pipeline.py`), after showing them which file will be wiped;
- ask whether to reopen the lesson page first or go straight to writing.

On a pass: mark it `passed` with `passed_at`, add it to `review` (it was learned from a worked
example), and offer `/teach-me` for the next one.
