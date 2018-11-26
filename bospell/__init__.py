from pathlib import Path
from typing import Dict, Union

from .a_preprocessing import corpus_cleanup, corpus_cleanup_vernacular
from .b_tokenizers import space_tok, pybo_tok, corpus_tok_to_correct, corpus_tok_vernacular
from .c_processors import pybo_error_types, pybo_error_concs, corpus_review_concs, corpus_correct_concs
from .d_formatters import basic_conc, stats_types


__all__ = ['SpellCheck']


components = {
    # Preprocessing
    'pre': {
        'pre_corpus': corpus_cleanup,
        'pre_vern': corpus_cleanup_vernacular,
    },
    # Tokenizers
    'tok': {
        'spaces': space_tok,
        'pybo': pybo_tok,
        'corpus_correct': corpus_tok_to_correct,
        'corpus_review': corpus_tok_vernacular
    },
    # Processors
    'proc': {
        'pybo_types': pybo_error_types,
        'pybo_concs': pybo_error_concs,
        'corpus_review': corpus_review_concs,
        'corpus_correct': corpus_correct_concs,
    },
    # Formatters
    'frm': {
        'conc': basic_conc,
        'types': stats_types
    }
}


class SpellCheck:
    def __init__(self, pipeline: Dict[str, Union[str, int]]):
        self.pre = None
        self.tok = None
        self.proc = None
        self.frm = None

        self.left = 5
        self.right = 5
        self.prof = None
        self.filename = None  # for an advanced mode, to show what conc comes from which file

        self.args_list = {'pre', 'tok', 'proc', 'frm',  # components
                          'pybo_profile',  # pybo
                          'left', 'right',  # concs
                          'filename'  # others
                          }
        self.parse_profile(pipeline)

    def parse_profile(self, pipeline):
        self.is_valid_params(pipeline)
        for arg, v in pipeline.items():
            if arg == 'pre':
                self.pre = v
            elif arg == 'tok':
                self.tok = v
            elif arg == 'proc':
                self.proc = v
            elif arg == 'frm':
                self.frm = v
            elif arg == 'pybo_profile':
                self.prof = v
            elif arg == 'left':
                self.left = v
            elif arg == 'right':
                self.right = v
            elif arg == 'filename':
                self.filename = v
        self.is_valid_pipeline()

    def is_valid_params(self, pipeline):
        for arg, val in pipeline.items():
            # ensure all arguments are valid attributes
            if arg not in self.args_list:
                raise SyntaxError(f'{arg} is not a valid argument\nvalid options are {" ".join(self.map)}')

            # ensure arguments have valid values
            if arg in components and val not in components[arg]:
                raise SyntaxError(f'{val} is not a valid value for {arg}\nvalid options are {" ".join(component[arg])}')

    def is_valid_pipeline(self):
        # missing pipes
        if not self.tok or not self.proc or not self.frm:
            raise BrokenPipeError('A valid pipeline must have a tokenizer, a processor and a formatter.')

        # detect pipeline inconsistencies through naming conventions
        if self.tok == 'pybo' and not self.prof:
            raise AttributeError('pybo tokenizer requires a profile as argument.')

        if (self.tok == 'pybo' and not self.proc.startswith('pybo')) \
           or (self.proc.startswith('pybo') and not self.tok == 'pybo'):
            raise BrokenPipeError('pybo tokenizer requires a pybo processor (both names start with "pybo").')

        if (self.proc.endswith('types') and not self.frm.endswith('types')) \
           or (self.frm.endswith('types') and not self.proc.endswith('types')):
            raise BrokenPipeError('types processor requires a types formatter (both names end with "types".')

        if (self.proc.endswith('concs') and not self.frm.endswith('concs')) \
           or (self.frm.endswith('concs') and not self.proc.endswith('concs')):
            raise BrokenPipeError('concs processor requires a concs formatter (both names end with "concs").')

    def check(self, text: str) -> str:
        if self.pre:
            text = components['pre'][self.pre](text)

        print('ok')
        if self.tok == 'pybo':
            elts = components['tok'][self.tok](text, self.prof)
        else:
            elts = components['tok'][self.tok](text)

        proc = components['proc'][self.proc]
        if self.proc.endswith('concs'):
            elts = proc(elts, left=self.left, right=self.right)
        else:
            elts = proc(elts)

        elts = components['frm'][self.frm](elts)

        return elts


# def spellcheck(string, preproc='', tok='', proc='', format='', left=5, right=5, filename=''):
#     elts = []
#
#     if preproc == 'corpus':
#         string = corpus_cleanup(string)
#
#     elif preproc == 'corpus_vernacular':
#         string = corpus_cleanup_vernacular(string)
#
#     if tok == 'sgmt_corpus':
#         elts = corpus_tok_to_correct(string)
#
#     elif tok == 'sgmt_corpus_vernacular':
#         elts = corpus_tok_vernacular(string)
#
#     elif tok == 'pybo':
#         elts = pybo_tok(string, 'GMD')
#
#     # compability check
#     if tok.startswith('pybo') and not proc.startswith('pybo'):
#         raise ValueError('tokens generated with pybo require matchers that support them.')
#
#     if proc == 'corpus_cor':
#         elts = prepare_sgmt_cor(elts, left=left, right=right)
#
#     elif proc == 'corpus_review_concs':
#         elts = prepare_sgmt_to_review(elts, left=left, right=right)
#
#     elif proc == 'corpus_vernacular':
#         elts = prepare_vernacular_to_review(elts, left=left, right=right)
#
#     elif proc == 'pybo_errors':
#         pass
#
#     elif proc == 'pybo_error_concs':
#         elts = prepare_error_concs(elts, left=left, right=right)
#
#     elif proc == 'pybo_error_types':
#         elts = prepare_error_types(elts)
#
#     if format == 'basic_conc':
#         elts = conc(elts)
#
#     elif format == 'types':
#         elts = format_types(elts)
#
#     return elts


# def spellcheck_folder(in_dir, out_dir, tok, proc, format, preproc='', left=5, right=5):
#     in_files = Path(in_dir).glob('*.txt')
#     total = []
#     for f in in_files:
#         print(f.name)
#         with f.open(encoding='utf-8-sig') as g:
#             dump = g.read()
#
#         out = spellcheck(dump, preproc, tok, proc, format, left=left, right=right)
#         total.append(out)
#
#     out_file = Path(out_dir) / 'total.tsv'
#     with out_file.open('w', encoding='utf-8-sig') as h:
#         h.write('\n'.join(total))
