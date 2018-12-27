from typing import List
from pathlib import Path
import re


def segment_with_tags(string, start_tag, end_tag, sep, in_tag_max=3):
    """segment a string on sep,
    yet keep everything between start and end tags in a single token.
    To avoid kilometric tokens, stop growing the token when sep has been encountered in_tag_max times.

    limitation: in case a token is truncated, it is left as is, without coming back and
    splitting it on the sep char.
    """
    chunks = []
    inside_tags = False
    chunk = ''
    sep_count = 0
    for char in string:
        if char == start_tag:
            inside_tags = True

        if inside_tags and char == sep:
            sep_count += 1

        if sep_count > in_tag_max:
            inside_tags = False
            sep_count = 0

        if inside_tags and char == end_tag:
            chunk += char
            chunks.append(chunk)
            chunk = ''
            inside_tags = False

        elif not inside_tags and char == sep:
            chunks.append(chunk)
            chunk = ''
            sep_count = 0

        else:
            chunk += char

    if chunk:
        chunks.append(chunk)

    return chunks


def apply_adjust(string):
    chunks = segment_with_tags(string, '[', ']', ' ')
    if not chunks:
        return string

    chunks = [c.replace(' ', '').strip('[]') for c in chunks]
    chunks = [c for c in chunks if c]
    return ' '.join(chunks)


def adjust_seg(tokens: List[str], sep: chr = ' ') -> str:
    out = sep.join(tokens)

    adjusts = {}
    lines = Path(Path(__file__).parent / '../resources/seg_adjust.csv').read_text().splitlines()
    for line in lines:
        cor, repl = line.split(',')
        orig = cor.replace('[', '').replace(']', '')
        cor = apply_adjust(cor)
        repl = apply_adjust(repl)
        if repl:
            adjusts[orig] = repl
        else:
            adjusts[orig] = cor

    normalisation = {}
    standardized = {}
    lines = Path(Path(__file__).parent / '../resources/vernacular.csv').read_text().splitlines()
    lines = [l for l in lines if not l.startswith(',')]
    for line in lines[1:]:
        normalized, to_normalize, standard = line.split(',')
        normalized, to_normalize, standard = normalized.rstrip('་').strip(), to_normalize.rstrip('་').strip(), standard.rstrip('་').strip()
        if normalized == to_normalize:
            continue
        normalisation[to_normalize] = normalized
        normalisation[to_normalize+'་'] = normalized+'་'
        if not standard or standard == to_normalize:
            continue
        standardized[to_normalize] = standard
        standardized[to_normalize+'་'] = standard+'་'

    for orig, repl in adjusts.items():
        out = out.replace(orig, repl)

    ### this part applies normalization after adjusting the segmentation
    # looping over standardized will apply standard equivalents of vernaculars instead of normalization
    for to_norm, normed in normalisation.items():
        to_norm = ' ' + to_norm + ' '
        normed = ' ' + normed + ' '
        out = out.replace(to_norm, normed)

    return out
