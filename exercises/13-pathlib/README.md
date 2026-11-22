# 13. Paths with pathlib

> **Your lesson:** [lessons/13-pathlib.md](../../lessons/13-pathlib.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A pipeline starts by finding its documents: every text file and PDF in a folder. It ends by writing files of its
own. `pathlib.Path` is how Python names files and folders: an object you join with `/`, ask for its parts, and
read and write through, the same on every operating system.

Documents are files whose suffix is `.txt`, `.md` or `.pdf`, in any case (`NOTES.TXT` counts).

Write four functions in `solution.py`. Every `folder`, `doc`, `out_dir` and `path` is a `Path`.

- `list_docs(folder)`: the names (`"returns.txt"`, not the whole path) of the documents directly in `folder`,
  sorted. Folders are left out even when their name ends in `.txt`, and so are files in subfolders.
- `all_docs(folder)`: the documents in `folder` and in every folder below it, each as its path relative to `folder`
  written with forward slashes (`"policies/warranty.txt"`), sorted.
- `output_path(doc, out_dir)`: where the chunks of `doc` are written: in `out_dir`, the document's name without its
  suffix, then `.chunks.jsonl`. Nothing is created; it only builds the `Path`.
- `save(path, text)`: writes `text` to `path` as UTF-8, creating any missing folders above it, replacing the file if
  it exists, and returns `path`.

```python
list_docs(Path("docs"))                                   # ["returns.txt", "shipping.pdf"]
all_docs(Path("docs"))                                    # ["policies/warranty.txt", "returns.txt", "shipping.pdf"]
output_path(Path("docs/shipping.pdf"), Path("out"))       # Path("out/shipping.chunks.jsonl")
save(Path("out/runs/today/notes.txt"), "café")            # Path("out/runs/today/notes.txt"), folders created
```

You will use: `folder.iterdir()`, `folder.rglob("*")`, `path.is_file()`, `path.name`, `path.stem`, `path.suffix`,
`path.relative_to(folder)`, `path.as_posix()`, `out_dir / name`, `path.parent.mkdir(parents=True, exist_ok=True)`,
`path.write_text(text, encoding="utf-8")`.
