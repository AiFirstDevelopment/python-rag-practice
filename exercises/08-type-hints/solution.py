# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
# Add a type hint to every parameter and return value, then write the bodies.

# EXERCISE-TODO: first_words(text, n=5): takes a str and an int, returns a str: the first n words of text joined by
# single spaces. Fewer than n words gives all of them. The default n stays 5.
#   first_words("You can return any unused item within 30 days.", 3)  ->  "You can return"
def first_words(text, n=5):
    raise NotImplementedError


# EXERCISE-TODO: page_lengths(pages): takes a list[str] (the text of each page), returns a dict[int, int]: page number,
# counted from 1, to the number of characters on that page. No pages gives an empty dict.
#   page_lengths(["Returns", "Shipping costs"])  ->  {1: 7, 2: 14}
def page_lengths(pages):
    raise NotImplementedError


# EXERCISE-TODO: longest_page(pages): takes a list[str], returns a tuple[int, str]: the page number (from 1) and text of
# the page with the most characters; the earliest one when two are equally long. Raises ValueError when pages is empty.
#   longest_page(["Returns", "Shipping costs"])  ->  (2, "Shipping costs")
def longest_page(pages):
    raise NotImplementedError
