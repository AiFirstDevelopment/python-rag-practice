# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.

# EXERCISE-TODO: parse_score(text): return the number in text (spaces around it allowed) as a float. Raise ValueError if
# it is not a number or is outside 0 to 1, with a message that contains the text you were given.
#   parse_score(" 0.8 ")  ->  0.8
#   parse_score("high")   ->  ValueError: not a score: 'high'
def parse_score(text: str) -> float:
    raise NotImplementedError


# EXERCISE-TODO: parse_all(texts): return a tuple (scores, errors): the scores that parsed, in order, and for each text
# that did not, its position in the list. Catch only ValueError, never everything.
#   parse_all(["0.9", "high", "1.5", "0"])  ->  ([0.9, 0.0], [1, 2])
def parse_all(texts: list[str]) -> tuple[list[float], list[int]]:
    raise NotImplementedError
