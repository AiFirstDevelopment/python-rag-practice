# 15. Reading a PDF's pages

Half of a company's documents are PDFs. A pipeline needs their text, and it needs to know which page each piece
came from, because an answer that cites "shipping.pdf, page 2" can be checked and one that cites nothing cannot.
`pypdf` opens a PDF and gives the text of each page.

Write two functions in `solution.py`. Every `path` is a `Path`.

- `pdf_pages(path)`: the text of each page of the PDF, in order, as a list of strings, with whitespace removed from
  both ends of each. A page with no text is an empty string in the list, so that the third page is still at
  position 2.
- `load_pages(path)`: the pages of any document as a list of `(page_number, text)` tuples, page numbers counted
  from 1.
  - A `.pdf` gives one tuple per page that has text. Pages without text are left out, and the other pages keep
    their real numbers.
  - A `.txt` or `.md` file is one page: `[(1, text)]`, read as UTF-8, whitespace removed from both ends; a file
    that is empty or only whitespace gives `[]`.
  - The suffix may be in any case (`.PDF`). Any other suffix raises `ValueError`.

```python
pdf_pages(Path("shipping.pdf"))
# ["Standard shipping takes 5 days.", "", "Express shipping costs $19.95."]
load_pages(Path("shipping.pdf"))
# [(1, "Standard shipping takes 5 days."), (3, "Express shipping costs $19.95.")]
load_pages(Path("returns.txt"))     # [(1, "You can return any unused item within 30 days.")]
load_pages(Path("logo.png"))        # ValueError
```

The tests build their own small PDFs, so there is no file to download.

You will use: `PdfReader(path)`, `reader.pages`, `page.extract_text()`, `str.strip`, `enumerate(pages, 1)`,
`path.suffix.lower()`, `path.read_text(encoding="utf-8")`.
