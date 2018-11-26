from typing import List


def space_tok(text: str) -> List[str]:
    """Tokenizes string on "\n" and spaces

    :param text: to tokenize
    :return: list of tokens
    """
    text = text.replace('\n', ' ')
    return text.split(' ')
