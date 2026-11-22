# 12. A module of your own, and imports

> **Your lesson:** [lessons/12-modules.md](../../lessons/12-modules.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A pipeline is not one file. Chunking, search and reranking each live in a module, and the file that runs the
pipeline imports from them. A module is nothing more than a `.py` file; importing it runs it once and gives you its
names.

This folder holds three files:

- `stopwords.py` is given. It defines `STOPWORDS`, a set of words that say nothing. Do not change it.
- `cleaning.py` does not exist yet. You create it, next to `solution.py`.
- `solution.py` is the script that uses both.

In `cleaning.py`, write:

- `clean(text)`: as in exercise 01, every run of whitespace becomes one space, none at either end.
- `content_words(text)`: the words of `text` as in exercise 04 (lowercased runs of letters, digits and apostrophes),
  in order, leaving out every word in `STOPWORDS`. Import `STOPWORDS` from `stopwords`; do not copy the set.

In `solution.py`:

- Import the two functions from `cleaning` (either `from cleaning import clean, content_words` or `import cleaning`).
  Do not write them again there.
- `summarize(text)`: returns a dict with two keys: `"text"`, the cleaned text, and `"words"`, its content words.
- When the file is run as a script (`uv run python solution.py` from this folder), it prints the cleaned `SAMPLE`,
  the constant at the top of the starter, and nothing else. When the file is imported, it prints nothing. That is
  what `if __name__ == "__main__":` is for.

```python
summarize("  The refund is\n in the mail. ")
# {"text": "The refund is in the mail.", "words": ["refund", "mail"]}
```

```
$ uv run python solution.py
Sale items can be returned within 14 days for store credit.
```

The tests import `cleaning` and `solution` with this folder on Python's search path, which is what Python does by
itself when you run a script from here.

You will use: a new file as a module, `from module import name`, `import module`, `if __name__ == "__main__":`.
