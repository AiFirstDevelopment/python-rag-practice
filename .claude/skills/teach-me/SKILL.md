---
name: teach-me
description: Teach the learner's current Python exercise by worked example - a rendered lesson in a VS Code tab with the solution's key parts highlighted, then they write it from scratch, get scored, and may restart until it is clean. Use when the learner types /teach-me, asks to be taught or shown an exercise first, or says they don't know where to start.
---

# /teach-me

Read `.claude/skills/TUTOR.md` (beside this skill's folder) first. Its voice, progress and order rules apply; its
"Never write their code" rule is relaxed only as this skill says.

## 1. Pick the exercise

The one they name, or `progress.json`'s `current`, or the next by TUTOR.md's "Order". Set `current`, mark it
`started`, and set `"taught": true` on it.

## 2. Build the lesson page

Read the exercise's `README.md` and its tests. Write a worked solution yourself and verify it passes the tests
(in the scratchpad, never in their file). Then write the lesson to `lessons/NN-slug.md` (gitignored, never inside
`exercises/`) and open it in VS Code: `"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" -r
lessons/NN-slug.md` (if not at that path, try `which code`). `.vscode/settings.json` maps `**/lessons/*.md` to
VS Code's built-in Markdown preview, so the tab shows only the rendered lesson, never the source. If that setting is
missing, add it back.

The lesson (Markdown; see `lessons/01-strings.md` if it exists for the shape):

- `# ` the exercise name. One short paragraph: what the code must do, from the README.
- The file it belongs in, in bold (`solution.py`; `cleaning.py` for 12; `pipeline.py` for 50; in module 4, 17-20,
  the example is *tests*, not code).
- The full worked solution as a raw HTML `<pre><code>` block (not a fenced block, which can't hold highlights), with
  line numbers typed at the start of each line and `<`, `&` escaped.
- The parts that carry the lesson wrapped in `<mark style="background:#ffeb3b;color:#000">`, each followed by
  `<b>[N]</b>`. Three to six marks.
- Under the code, one note per mark starting `**[N]**`: what that part does and the Python idea behind it, two or
  three sentences. Plain engineer-to-engineer voice.
- A rule, then: "**Close this page and write it from memory in `solution.py`. When you are done, save it and type `/check` in the Claude chat.**"

## 3. Hand over

In the chat, one line saying the lesson is open in a tab and how many parts are
highlighted, then ask: "Ready to write it
yourself?" Do not paste the solution in the chat.

## 4. Score their attempt

When they say they're done (or type /check), run `uv run pytest exercises/NN-slug` and read their file. Report:

- Score: tests passed out of total.
- Where it went wrong: for each failing test, the input, what was expected, what came back, and the line in their
  file that causes it (as a clickable path with line number). Name the cause plainly; since they have seen the
  solution, you may compare to the lesson's marked part by number ("see mark 2").
- If all pass, say "passed", and at most one idiom note per TUTOR.md's "On a pass".

Record `checks` and the mistakes in `progress.json`. Do not edit their file to fix it.

## 5. Offer the restart

If any test failed, or they passed but want it cleaner: "Restart this exercise from scratch?" On a yes, and only
then:

- reset their file to the starter with `git checkout -- exercises/NN-slug/solution.py` (for 12, also delete
  `cleaning.py`; for 50, delete `pipeline.py`), after showing them which file will be wiped;
- ask whether to reopen the lesson page first or go straight to writing.

On a pass with no restart wanted: mark it `passed` with `passed_at`, add it to `review` (it was learned from a worked
example), and offer `/teach-me` or `/practice` for the next one.
