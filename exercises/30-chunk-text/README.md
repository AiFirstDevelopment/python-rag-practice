# 30. Chunk text at sentence ends

A pipeline does not search whole documents; it searches pieces of them, called chunks, and sends the best few to the
model. A chunk cut in the middle of a sentence loses its meaning at both ends, so the cut goes at a sentence end
whenever one is near enough.

Write `chunk_page(text)` in `solution.py`: the text of one page cut into a list of pieces of at most `CHUNK_CHARS`
(900) characters. The rule, exactly as the course's `rag/chunks.py` has it:

1. Strip the whitespace from both ends of the text. What is left is the rest.
2. While the rest is longer than 900 characters, look at its first 900 characters (the window) and choose where to
   cut:
   - Find the last sentence end in the window. A sentence end is one of `.`, `?` or `!` followed by a space or a line
     break (the six pairs in `ENDS`); both characters must be inside the window. If its punctuation mark is past the
     halfway mark (at an index greater than 450), cut just after the mark, so the piece ends with it.
   - Otherwise cut at the last space in the window (the piece ends before that space), if there is one.
   - Otherwise (no space at all) cut at 900 characters.

   The piece is the rest up to the cut, stripped; the new rest is what follows the cut, stripped.
3. When the rest is 900 characters or fewer, it is the last piece, unless it is empty.

So a text of 900 characters or fewer is one piece, an empty or all-whitespace text gives `[]`, and a sentence end in
the first half of the window is ignored (cutting there would make a piece too small).

```python
chunk_page("  One sentence.  ")            # ["One sentence."]
chunk_page("x" * 2000)                     # three pieces of 900, 900 and 200 characters
chunk_page("a" * 500 + ". " + "b " * 300)  # the first piece is "aaa...a." (501 characters)
```

You will use: a `while` loop, slicing, `str.rfind` (it returns -1 when it finds nothing), `max`, `str.strip`.
