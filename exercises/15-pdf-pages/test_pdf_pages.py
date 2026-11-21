import importlib.util
from pathlib import Path

import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

PAGES = ["Standard shipping takes 5 days.", "", "Express shipping costs $19.95."]


def make_pdf(path, pages):
    """A PDF with one page per string, written with pypdf alone. An empty string makes a page with no text."""
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica")}))
    for text in pages:
        page = writer.add_blank_page(width=612, height=792)
        if text:
            stream = DecodedStreamObject()
            stream.set_data(f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode())
            page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
            page[NameObject("/Contents")] = writer._add_object(stream)
    with open(path, "wb") as file:
        writer.write(file)
    return path


@pytest.fixture
def pdf(tmp_path):
    return make_pdf(tmp_path / "shipping.pdf", PAGES)


def test_pdf_pages_gives_the_text_of_each_page_in_order(tmp_path):
    path = make_pdf(tmp_path / "two.pdf", ["Returns within 30 days.", "Sale items are final."])
    assert solution.pdf_pages(path) == ["Returns within 30 days.", "Sale items are final."]


def test_pdf_pages_keeps_a_page_without_text_as_an_empty_string(pdf):
    assert solution.pdf_pages(pdf) == PAGES


def test_pdf_pages_strips_the_ends_of_each_page(tmp_path):
    path = make_pdf(tmp_path / "padded.pdf", ["   Padded page.   "])
    assert solution.pdf_pages(path) == ["Padded page."]


def test_load_pages_of_a_pdf_skips_empty_pages_and_keeps_real_page_numbers(pdf):
    assert solution.load_pages(pdf) == [(1, PAGES[0]), (3, PAGES[2])]


def test_load_pages_of_a_text_file_is_one_page(tmp_path):
    path = tmp_path / "returns.txt"
    path.write_text("\nYou can return any unused item within 30 days. Café vouchers too.\n\n", encoding="utf-8")
    assert solution.load_pages(path) == [(1, "You can return any unused item within 30 days. Café vouchers too.")]
    markdown = tmp_path / "rewards.md"
    markdown.write_text("# Rewards\n\nOne point per dollar.\n", encoding="utf-8")
    assert solution.load_pages(markdown) == [(1, "# Rewards\n\nOne point per dollar.")]


def test_load_pages_of_an_empty_text_file_is_no_pages(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("  \n", encoding="utf-8")
    assert solution.load_pages(path) == []


def test_load_pages_accepts_a_suffix_in_any_case(tmp_path):
    path = make_pdf(tmp_path / "SHIPPING.PDF", PAGES[:1])
    assert solution.load_pages(path) == [(1, PAGES[0])]


def test_load_pages_refuses_other_kinds_of_file(tmp_path):
    path = tmp_path / "logo.png"
    path.write_bytes(b"not a document")
    with pytest.raises(ValueError):
        solution.load_pages(path)
