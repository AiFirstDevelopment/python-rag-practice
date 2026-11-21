import re


def clean(text: str) -> str:
    return re.sub(r" +", " ", text).strip()


def preview(text: str, n: int) -> str:
    return text[:n] + "..." if len(text) > n else text
