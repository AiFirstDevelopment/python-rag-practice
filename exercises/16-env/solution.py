# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import os
from pathlib import Path

from dotenv import load_dotenv

# Given: the model used when PRACTICE_MODEL is not set.
DEFAULT_MODEL = "practice-model-1"


# get_setting(name, default=None): return the value of the environment variable name. When it is not set, or set to
# an empty string, return default; when there is no default either (None), raise RuntimeError with a message that
# contains name.
#   get_setting("PRACTICE_MODEL", "small")  ->  "small"   (when the variable is not set)
def get_setting(name: str, default: str | None = None) -> str:
    raise NotImplementedError


# load_env(path): load the .env file at path (lines of NAME=value) into the environment. A variable that is already
# set in the environment keeps its value: the real environment wins over the file. A file that does not exist is not
# an error; nothing is loaded.
def load_env(path: Path) -> None:
    raise NotImplementedError


# read_config(env_file=None): load env_file when one is given, then return a dict with three keys:
#   "api_key": PRACTICE_API_KEY, required (no default, so RuntimeError when missing);
#   "model": PRACTICE_MODEL, or DEFAULT_MODEL when not set;
#   "top_k": PRACTICE_TOP_K as an int, or 5 when not set; a value that is not a whole number raises ValueError.
#   read_config(Path(".env"))  ->  {"api_key": "sk-test-1234567890", "model": "practice-model-1", "top_k": 8}
def read_config(env_file: Path | None = None) -> dict:
    raise NotImplementedError


# mask(secret): return the secret made safe to print in a log: its first 4 characters followed by "...". A secret of
# 8 characters or fewer gives just "...".
#   mask("sk-test-1234567890")  ->  "sk-t..."
def mask(secret: str) -> str:
    raise NotImplementedError
