# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.

# EXERCISE-TODO: top_words(text, n, stopwords): return the n most frequent words of text that are not in stopwords, as a
# list of (word, count) tuples, most frequent first; words with the same count in alphabetical order. Words are found as
# in exercise 04 (lowercased runs of letters, digits and apostrophes); stopwords may be in any case. Write the word
# splitting again here; this file stands alone.
#   top_words("The refund is a refund. The receipt is the proof.", 2, {"the", "is", "a"})
#     ->  [("refund", 2), ("proof", 1)]
def top_words(text: str, n: int, stopwords: set[str]) -> list[tuple[str, int]]:
    raise NotImplementedError
