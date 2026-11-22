# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.

# clean(text): return the text with every run of whitespace (spaces, tabs, line breaks) turned into one space,
# and no whitespace at either end.
#   clean("  Returns are\n accepted   within 30 days. ")  ->  "Returns are accepted within 30 days."
def clean(text: str) -> str:
    raise NotImplementedError


# preview(text, n): return the first n characters of text. If the text was longer than n, add "..." after
# those n characters; if not, return it unchanged.
#   preview("Returns are accepted", 7)  ->  "Returns..."
#   preview("Short", 10)                ->  "Short"
def preview(text: str, n: int) -> str:
    raise NotImplementedError
