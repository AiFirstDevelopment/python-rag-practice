def clean(text: str) -> str:
    return " ".join(text.split())


def preview(text: str, n: int) -> str:
    return text[:n] + "..." if len(text) > n else text
