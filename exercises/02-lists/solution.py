# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.

# EXERCISE-TODO: window(items, i, radius): return the items from position i - radius to i + radius, both included, as a
# new list. Near either end, take what exists instead of failing or wrapping around. Do not change the list you were
# given.
#   window(["a", "b", "c", "d", "e"], 2, 1)  ->  ["b", "c", "d"]
#   window(["a", "b", "c", "d", "e"], 0, 2)  ->  ["a", "b", "c"]
#   window(["a", "b", "c", "d", "e"], 4, 1)  ->  ["d", "e"]
def window(items: list, i: int, radius: int) -> list:
    raise NotImplementedError
