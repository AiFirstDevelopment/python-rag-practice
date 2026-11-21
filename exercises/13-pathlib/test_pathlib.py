import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


@pytest.fixture
def docs(tmp_path):
    folder = tmp_path / "docs"
    (folder / "policies" / "old").mkdir(parents=True)
    (folder / "archive.txt").mkdir()                      # a folder whose name looks like a document
    for name in ["shipping.pdf", "returns.txt", "rewards.md", "NOTES.TXT", "logo.png", "data.json",
                 "policies/warranty.txt", "policies/old/warranty-2019.pdf", "policies/draft.docx"]:
        (folder / name).write_text("x", encoding="utf-8")
    return folder


def test_list_docs_gives_sorted_names_of_documents_only(docs):
    assert solution.list_docs(docs) == sorted(["NOTES.TXT", "returns.txt", "rewards.md", "shipping.pdf"])


def test_list_docs_leaves_out_folders_and_what_is_inside_them(docs):
    names = solution.list_docs(docs)
    assert "archive.txt" not in names and "policies" not in names and "warranty.txt" not in names


def test_list_docs_of_an_empty_folder(tmp_path):
    assert solution.list_docs(tmp_path) == []


def test_all_docs_goes_into_subfolders_and_gives_relative_paths(docs):
    assert solution.all_docs(docs) == sorted([
        "NOTES.TXT", "policies/old/warranty-2019.pdf", "policies/warranty.txt", "returns.txt", "rewards.md",
        "shipping.pdf"])


def test_output_path_swaps_the_suffix_and_the_folder():
    assert solution.output_path(Path("docs/shipping.pdf"), Path("out")) == Path("out/shipping.chunks.jsonl")
    assert solution.output_path(Path("/data/docs/policies/warranty.txt"), Path("out/run1")) == Path(
        "out/run1/warranty.chunks.jsonl")


def test_save_creates_missing_folders_and_returns_the_path(tmp_path):
    path = tmp_path / "out" / "runs" / "today" / "notes.txt"
    assert solution.save(path, "café\nsecond line\n") == path
    assert path.read_text(encoding="utf-8") == "café\nsecond line\n"


def test_save_replaces_an_existing_file(tmp_path):
    path = tmp_path / "notes.txt"
    solution.save(path, "first, and longer")
    solution.save(path, "second")
    assert path.read_text(encoding="utf-8") == "second"
