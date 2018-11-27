from typing import List

from .helpers import segment_with_tags


def corpus_tok_to_correct(text: str) -> List[str]:
    """Tokenizes on spaces and \n, while keeping together the content of [ and ] tags

    :param text: to tokenize
    :return: list of tokens
    """
    text = text.replace('\n', ' ')
    text = text.replace('_', '_ ')  # so that spaces in orig string is used
    return segment_with_tags(text, '[', ']', ' ')


def corpus_tok_vernacular(text: str) -> List[str]:
    """Tokenizes on spaces and \n, while keeping together the content of ༺ and ༻ tags

    :param text: to tokenize
    :return: list of tokens
    """
    text = text.replace('\n', ' ')
    text = text.replace('_', '_ ')  # so that spaces in orig string is used
    return segment_with_tags(text, '༺', '༻', ' ')
