# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from pathlib import Path

from pypdf import PdfReader


# pdf_pages(path): return the text of each page of the PDF at path, in order, as a list of strings, with whitespace
# removed from both ends of each. A page with no text is an empty string in the list, so that the third page is
# still at position 2.
#   pdf_pages(Path("shipping.pdf"))  ->  ["Standard shipping takes 5 days.", "", "Express shipping costs $19.95."]
def pdf_pages(path: Path) -> list[str]:
    raise NotImplementedError


# load_pages(path): return the pages of any document as a list of (page_number, text) tuples, page numbers counted
# from 1. A .pdf gives one tuple per page that has text; pages without text are left out, and the other pages keep
# their real numbers. A .txt or .md file is one page: [(1, text)], read as UTF-8, whitespace removed from both ends;
# a file that is empty or only whitespace gives []. The suffix may be in any case (.PDF). Any other suffix raises
# ValueError.
#   load_pages(Path("shipping.pdf"))
#     ->  [(1, "Standard shipping takes 5 days."), (3, "Express shipping costs $19.95.")]
#   load_pages(Path("returns.txt"))   ->  [(1, "You can return any unused item within 30 days.")]
#   load_pages(Path("logo.png"))      ->  ValueError
def load_pages(path: Path) -> list[tuple[int, str]]:
    raise NotImplementedError
