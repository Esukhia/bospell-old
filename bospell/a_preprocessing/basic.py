import re


def basic_cleanup(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text
