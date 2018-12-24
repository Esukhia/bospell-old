import re

VERNACULAR = ['༺', '༻']
CORRECTIONS = ['[', ']']
OTHERS = ['༼', '༽', '༜', '༙', '#', '$']
TIMECODES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', ':', '-', '>']


def corpus_cleanup(text: str) -> str:
    to_remove = VERNACULAR + OTHERS
    text = re.sub(r'༺(.+?)།.+?༻', r'\1', text)
    for t in to_remove:
        text = text.replace(t, '')
    text = re.sub(r'\s+', r' ', text)
    return text


def corpus_cleanup_vernacular(text: str) -> str:
    """Does the following:
        - deletes the literary equivalent/translation of vernacular words
        - deletes all corpus markup except for the vernacular parenthesis
    """
    to_remove = CORRECTIONS + OTHERS
    text = re.sub(r'༺(.+?)།.+?༻', r'༺\1༻', text)
    for t in to_remove:
        text = text.replace(t, '')
    text = re.sub(r'\s+', r' ', text)
    return text


def corpus_clean_all(text: str) -> str:
    to_remove = VERNACULAR + CORRECTIONS + OTHERS + TIMECODES + ['_']
    for t in to_remove:
        text = text.replace(t, ' ')
    text = re.sub(r'\s+', r' ', text)
    return text
