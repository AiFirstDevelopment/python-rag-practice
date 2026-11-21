import importlib
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))       # so `import cleaning` and `import stopwords` find the files in this folder

_spec = importlib.util.spec_from_file_location("solution", HERE / "solution.py")
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

CLEANED_SAMPLE = "Sale items can be returned within 14 days for store credit."


def cleaning():
    return importlib.import_module("cleaning")


def test_cleaning_module_has_clean():
    assert cleaning().clean("  The refund is\n in the\tmail. ") == "The refund is in the mail."


def test_content_words_are_lowercased_and_leave_out_stopwords():
    assert cleaning().content_words("The refund is in the mail.") == ["refund", "mail"]
    assert cleaning().content_words("Don't return THE gift card, 30 days!") == ["don't", "return", "gift", "card", "30", "days"]


def test_cleaning_imports_the_given_stopwords_instead_of_copying_them():
    import stopwords
    module = cleaning()
    assert getattr(module, "STOPWORDS", None) is stopwords.STOPWORDS or getattr(module, "stopwords", None) is stopwords


def test_summarize_returns_the_clean_text_and_its_content_words():
    assert solution.summarize("  The refund is\n in the mail. ") == {
        "text": "The refund is in the mail.", "words": ["refund", "mail"]}


def test_solution_imports_from_cleaning_instead_of_defining_its_own():
    module = cleaning()
    imported_names = (getattr(solution, "clean", None) is module.clean
                      and getattr(solution, "content_words", None) is module.content_words)
    assert imported_names or getattr(solution, "cleaning", None) is module


def test_run_as_a_script_it_prints_the_cleaned_sample():
    run = subprocess.run([sys.executable, "solution.py"], cwd=HERE, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert run.stdout.strip() == CLEANED_SAMPLE


def test_imported_it_prints_nothing(capsys):
    spec = importlib.util.spec_from_file_location("solution_again", HERE / "solution.py")
    spec.loader.exec_module(importlib.util.module_from_spec(spec))
    assert capsys.readouterr().out == ""
    assert callable(solution.summarize) and solution.summarize("The mail")["words"] == ["mail"]
