from typing import List, Tuple

from .helpers import find_context_sizes


def is_correction(token):
    return '[' in token or ']' in token


def is_to_merge(token):
    return token.startswith('[') \
           and token.count('[') == 1 \
           and token.endswith(']') \
           and token.count(']') == 1 \
           and ' ' in token


def find_to_review(tokens):
    to_review = {}
    for token in tokens:
        if is_to_merge(token):
            match = token[1:-1].split(' ')
            to_review[token] = match

    return to_review


def corpus_review_concs(tokens: List[str], left=5, right=5) -> List[Tuple[List[str], str, List[str]]]:
    to_review = find_to_review(tokens)
    concs = []
    for orig, splitted in to_review.items():
        s = len(splitted)
        for i in range(len(tokens)):
            l_size, r_size = -1, -1
            if tokens[i] == orig:
                l_size, r_size = find_context_sizes(i, left, right, len(tokens))
            elif tokens[i:i + s] == splitted:
                l_size, r_size = find_context_sizes(i + 1, left, right, len(tokens))

            conc = (tokens[l_size:i], tokens[i], tokens[i+1:r_size])
            concs.append(conc)

    return concs


def corpus_correct_concs(tokens: List[str], left=5, right=5) -> List[Tuple[List[str], str, List[str]]]:
    concs = []
    for i in range(len(tokens)):
        token = tokens[i]
        if is_correction(token):
            l_size, r_size = find_context_sizes(i, left, right, len(tokens))
            conc = (tokens[l_size:i], token, tokens[i+1:r_size])
            concs.append(conc)

    return concs


def corpus_adjust_segmentation(tokens: List[str]) -> List[str]:
    out = []

    return out
