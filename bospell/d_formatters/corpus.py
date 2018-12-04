from typing import List
from pathlib import Path


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

    for orig, repl in adjusts.items():
        out = out.replace(orig, repl)

    return out
