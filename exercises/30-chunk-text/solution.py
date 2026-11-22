# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
CHUNK_CHARS = 900
ENDS = (". ", "? ", "! ", ".\n", "?\n", "!\n")


# EXERCISE-TODO: chunk_page(text): return the text of one page cut into a list of pieces of at most CHUNK_CHARS (900)
# characters. Strip the whitespace from both ends; what is left is the rest. While the rest is longer than 900, look at
# its first 900 characters (the window) and cut: just after the last sentence end in the window (one of the six ENDS
# pairs, both characters inside the window) if its mark is at an index greater than 450; otherwise at the last space in
# the window (the piece ends before that space); otherwise (no space) at 900. The piece is the rest up to the cut,
# stripped; the new rest is what follows the cut, stripped. When the rest is 900 or fewer, it is the last piece, unless
# it is empty. A text of 900 or fewer is one piece; an empty or all-whitespace text gives [].
#   chunk_page("  One sentence.  ")            ->  ["One sentence."]
#   chunk_page("x" * 2000)                     ->  three pieces of 900, 900 and 200 characters
#   chunk_page("a" * 500 + ". " + "b " * 300)  ->  the first piece is "aaa...a." (501 characters)
def chunk_page(text: str) -> list[str]:
    raise NotImplementedError
