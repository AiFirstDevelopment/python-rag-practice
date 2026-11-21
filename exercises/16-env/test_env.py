import importlib.util
import os
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

NAMES = ["PRACTICE_API_KEY", "PRACTICE_MODEL", "PRACTICE_TOP_K"]


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    """Every test starts with the three variables unset, and whatever it or load_dotenv sets is undone after it."""
    for name in NAMES:
        monkeypatch.setenv(name, "placeholder")
        monkeypatch.delenv(name)


def env_file(tmp_path, text):
    path = tmp_path / ".env"
    path.write_text(text, encoding="utf-8")
    return path


def test_get_setting_reads_the_variable(monkeypatch):
    monkeypatch.setenv("PRACTICE_MODEL", "big-model")
    assert solution.get_setting("PRACTICE_MODEL") == "big-model"
    assert solution.get_setting("PRACTICE_MODEL", "small") == "big-model"


def test_get_setting_falls_back_to_the_default_when_unset_or_empty(monkeypatch):
    assert solution.get_setting("PRACTICE_MODEL", "small") == "small"
    monkeypatch.setenv("PRACTICE_MODEL", "")
    assert solution.get_setting("PRACTICE_MODEL", "small") == "small"


def test_get_setting_without_a_default_raises_and_names_the_variable(monkeypatch):
    with pytest.raises(RuntimeError, match="PRACTICE_API_KEY"):
        solution.get_setting("PRACTICE_API_KEY")
    monkeypatch.setenv("PRACTICE_API_KEY", "")
    with pytest.raises(RuntimeError, match="PRACTICE_API_KEY"):
        solution.get_setting("PRACTICE_API_KEY")


def test_load_env_puts_the_file_into_the_environment(tmp_path):
    solution.load_env(env_file(tmp_path, "PRACTICE_API_KEY=sk-test-1234567890\nPRACTICE_TOP_K=8\n"))
    assert os.environ["PRACTICE_API_KEY"] == "sk-test-1234567890"
    assert os.environ["PRACTICE_TOP_K"] == "8"


def test_load_env_lets_the_real_environment_win_and_ignores_a_missing_file(tmp_path, monkeypatch):
    monkeypatch.setenv("PRACTICE_MODEL", "from-environment")
    solution.load_env(env_file(tmp_path, "PRACTICE_MODEL=from-file\n"))
    assert os.environ["PRACTICE_MODEL"] == "from-environment"
    solution.load_env(tmp_path / "missing" / ".env")
    assert "PRACTICE_API_KEY" not in os.environ


def test_read_config_reads_the_file_and_converts_top_k(tmp_path):
    path = env_file(tmp_path, "PRACTICE_API_KEY=sk-test-1234567890\nPRACTICE_MODEL=big-model\nPRACTICE_TOP_K=8\n")
    assert solution.read_config(path) == {"api_key": "sk-test-1234567890", "model": "big-model", "top_k": 8}


def test_read_config_uses_defaults_and_requires_the_key(monkeypatch):
    with pytest.raises(RuntimeError, match="PRACTICE_API_KEY"):
        solution.read_config()
    monkeypatch.setenv("PRACTICE_API_KEY", "sk-test-1234567890")
    assert solution.read_config() == {
        "api_key": "sk-test-1234567890", "model": solution.DEFAULT_MODEL, "top_k": 5}
    monkeypatch.setenv("PRACTICE_TOP_K", "lots")
    with pytest.raises(ValueError):
        solution.read_config()


def test_mask_shows_four_characters_of_a_long_secret_and_none_of_a_short_one():
    assert solution.mask("sk-test-1234567890") == "sk-t..."
    assert solution.mask("12345678") == "..."
    assert solution.mask("123456789") == "1234..."
    assert solution.mask("") == "..."
