from pathlib import Path

from .formatters import conc
from .matchers import corpus_sgmt_cor
from .tokenizers import basic, segmt_corpus

__all__ = ['spellcheck', 'spellcheck_folder']


def spellcheck(string, tok='', matcher='', format=''):
    elts = []

    if tok == 'sgmt_corpus':
        elts = segmt_corpus(string)

    if matcher == 'corpus_cor':
        elts = corpus_sgmt_cor(elts)

    if format == 'conc':
        elts = conc(elts)

    return elts


def spellcheck_folder(in_dir, out_dir, tok, matcher, format):
    in_files = Path(in_dir).glob('*.txt')
    total = []
    for f in in_files:
        print(f.name)
        with f.open(encoding='utf-8-sig') as g:
            dump = g.read()

        out = spellcheck(dump, tok, matcher, format)
        total.append(out)

    out_file = Path(out_dir) / 'total.txt'
    with out_file.open('w', encoding='utf-8-sig') as h:
        h.write('\n'.join(total))
