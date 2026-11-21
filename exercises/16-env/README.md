# 16. Environment variables and a .env file

A pipeline that calls a model needs an API key, and a key must never be written in the code or committed. It lives
in an environment variable; on your own machine, in a file named `.env` that git ignores and that `python-dotenv`
loads into the environment when the program starts. Settings you want to change without editing code (which model,
how many passages) travel the same way.

A `.env` file is lines of `NAME=value`:

```
PRACTICE_API_KEY=sk-test-1234567890
PRACTICE_TOP_K=8
```

Write four functions in `solution.py`:

- `get_setting(name, default=None)`: the value of the environment variable `name`. When it is not set, or set to an
  empty string, the result is `default`; and when there is no default either (`None`), it raises `RuntimeError`
  with a message that contains `name`.
- `load_env(path)`: loads the `.env` file at `path` into the environment. A variable that is already set in the
  environment keeps its value: the real environment wins over the file. A file that does not exist is not an
  error; nothing is loaded.
- `read_config(env_file=None)`: loads `env_file` when one is given, then returns a dict with three keys:
  - `"api_key"`: `PRACTICE_API_KEY`, required (no default, so `RuntimeError` when missing);
  - `"model"`: `PRACTICE_MODEL`, or `DEFAULT_MODEL` (given in the starter) when not set;
  - `"top_k"`: `PRACTICE_TOP_K` as an `int`, or `5` when not set. Environment variables are always strings, so it
    must be converted; a value that is not a whole number raises `ValueError`.
- `mask(secret)`: a key made safe to print in a log: its first 4 characters followed by `...`. A secret of 8
  characters or fewer gives just `...`, so a short one is not given away.

```python
get_setting("PRACTICE_MODEL", "small")     # "small" when the variable is not set
read_config(Path(".env"))
# {"api_key": "sk-test-1234567890", "model": "practice-model-1", "top_k": 8}
mask("sk-test-1234567890")                 # "sk-t..."
```

The tests set and unset variables for one test at a time and write their `.env` files in a temporary folder; your
own environment and files are not touched.

You will use: `os.environ.get(name)`, `load_dotenv(path)` from `dotenv`, `int(...)`, `raise RuntimeError(...)`,
slicing.
