# 01. Strings

> **Your lesson:** [lessons/01-strings.md](../../lessons/01-strings.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Text pulled out of a PDF is messy: line breaks in the middle of sentences, runs of spaces, spaces at the ends. Before
a pipeline cuts text into chunks, it cleans it.

Write two functions in `solution.py`:

- `clean(text)` returns the text with every run of whitespace (spaces, tabs, line breaks) turned into one space, and
  no whitespace at either end.
- `preview(text, n)` returns the first `n` characters of `text`; if the text was longer than `n`, it ends with `...`
  added after those `n` characters.

```python
clean("  Returns are\n accepted   within 30 days. ")  # "Returns are accepted within 30 days."
preview("Returns are accepted", 7)                    # "Returns..."
preview("Short", 10)                                  # "Short"
```

You will use: string methods, slicing, `len`, f-strings.
