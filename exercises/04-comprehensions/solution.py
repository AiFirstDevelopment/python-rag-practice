# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.

# EXERCISE-TODO: words(text): return the words of text, lowercased, in order. A word is a run of letters, digits or
# apostrophes; every other character separates words. Use list and dict comprehensions where they fit.
#   words("Refunds: 30 days, no receipt? Don't worry.")
#     ->  ["refunds", "30", "days", "no", "receipt", "don't", "worry"]
def words(text: str) -> list[str]:
    raise NotImplementedError


# EXERCISE-TODO: keyword_hits(text, keywords): return a dict from each keyword (as given) to how many times it appears
# in words(text), ignoring case. Keywords that never appear map to 0.
#   keyword_hits("Refund or refund? REFUND!", ["refund", "Receipt"])  ->  {"refund": 3, "Receipt": 0}
def keyword_hits(text: str, keywords: list[str]) -> dict[str, int]:
    raise NotImplementedError
