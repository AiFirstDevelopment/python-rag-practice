import os
from pathlib import Path

from dotenv import load_dotenv

# Given: the model used when PRACTICE_MODEL is not set.
DEFAULT_MODEL = "practice-model-1"


def get_setting(name: str, default: str | None = None) -> str:
    raise NotImplementedError


def load_env(path: Path) -> None:
    raise NotImplementedError


def read_config(env_file: Path | None = None) -> dict:
    raise NotImplementedError


def mask(secret: str) -> str:
    raise NotImplementedError
