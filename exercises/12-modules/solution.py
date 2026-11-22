# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
# Given: the text this file prints, cleaned, when it is run as a script.
SAMPLE = "  Sale items can be returned\n within 14 days   for store credit.  "

# Import clean and content_words from your cleaning.py here.


# EXERCISE-TODO: summarize(text): return a dict with two keys: "text", the cleaned text, and "words", its content words.
# Use clean and content_words imported from cleaning; do not write them again here.
#   summarize("  The refund is\n in the mail. ")
#     ->  {"text": "The refund is in the mail.", "words": ["refund", "mail"]}
def summarize(text: str) -> dict:
    raise NotImplementedError


# When this file is run as a script, print the cleaned SAMPLE.
