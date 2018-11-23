from pathlib import Path

from .a_preprocessing import corpus_cleanup
from .b_tokenizers import basic, segmt_corpus, tok_pybo
from .c_matchers import corpus_sgmt_cor, corpus_sgmt_to_review1
from .d_formatters import conc


__all__ = ['spellcheck', 'spellcheck_folder']


def spellcheck(string, preproc='', tok='', matcher='', format='', left=5, right=5):
    elts = []

    if preproc == 'corpus':
        string = corpus_cleanup(string)

    if tok == 'sgmt_corpus':
        elts = segmt_corpus(string)
    elif tok == 'pybo':
        elts = tok_pybo(string, 'GMD')

    # compability check
    if tok.startswith('pybo') and matcher.startswith('pybo'):
        raise ValueError('tokens generated with pybo require matchers that support them.')

    if matcher == 'corpus_cor':
        elts = corpus_sgmt_cor(elts, left=left, right=right)
    elif matcher == 'corpus_to_review':
        elts = corpus_sgmt_to_review1(elts, left=left, right=right)
    elif matcher == 'pybo_errors':
        pass

    if format == 'conc':
        elts = conc(elts)

    return elts


def spellcheck_folder(in_dir, out_dir, tok, matcher, format, preproc='', left=5, right=5):
    in_files = Path(in_dir).glob('*.txt')
    total = []
    for f in in_files:
        print(f.name)
        with f.open(encoding='utf-8-sig') as g:
            dump = g.read()

        out = spellcheck(dump, preproc, tok, matcher, format, left=left, right=right)
        total.append(out)

    out_file = Path(out_dir) / 'total.tsv'
    with out_file.open('w', encoding='utf-8-sig') as h:
        h.write('\n'.join(total))
