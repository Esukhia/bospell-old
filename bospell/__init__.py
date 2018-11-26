from pathlib import Path

from .a_preprocessing import basic_cleanup, corpus_cleanup, corpus_cleanup_vernacular
from .b_tokenizers import space_tok, pybo_tok, corpus_tok_to_correct, corpus_tok_vernacular
from .c_processors import spaces_plain_fulltext, pybo_raw_content, pybo_raw_types, pybo_error_types, pybo_error_concs, \
    corpus_review_concs, corpus_correct_concs
from .d_formatters import plaintext, basic_conc, stats_types

from .config import Config

__all__ = ['SpellCheck', 'CheckFile']


components = {
    # a. Preprocessing
    'pre': {
        'pre_basic': basic_cleanup,
        'pre_corpus': corpus_cleanup,
        'pre_vern': corpus_cleanup_vernacular,
    },
    # b. Tokenizers
    'tok': {
        'spaces': space_tok,
        'pybo': pybo_tok,
        'corpus_correct': corpus_tok_to_correct,
        'corpus_review': corpus_tok_vernacular
    },
    # c. Processors
    'proc': {
        'spaces_fulltext': spaces_plain_fulltext,
        'pybo_raw_content': pybo_raw_content,
        'pybo_raw_types': pybo_raw_types,
        'pybo_types': pybo_error_types,
        'pybo_concs': pybo_error_concs,
        'corpus_review': corpus_review_concs,
        'corpus_correct': corpus_correct_concs,
    },
    # d. Formatters
    'frm': {
        'plaintext': plaintext,
        'concs': basic_conc,
        'types': stats_types
    }
}


class SpellCheck:
    def __init__(self, profile):
        self.pre = None
        self.tok = None
        self.proc = None
        self.frm = None

        self.left = 5
        self.right = 5
        self.prof = None
        self.filename = None  # for an advanced mode, to show what conc comes from which file

        self.args_list = {
                          'pre', 'tok', 'proc', 'frm',  # components
                          'pybo_profile',               # pybo
                          'left', 'right',              # concs
                          'filename'                    # others
                          }

        self.config = Config('bospell.yaml')
        self.parse_profile(self.config.get_profile(profile))

    def check(self, text: str) -> str:
        # a. preprocessing
        if self.pre:
            text = components['pre'][self.pre](text)

        # b. tokenizing
        if self.tok == 'pybo':
            elts = components['tok'][self.tok](text, self.prof)
        else:
            elts = components['tok'][self.tok](text)

        # c. processing
        proc = components['proc'][self.proc]
        if self.proc.endswith('concs'):
            elts = proc(elts, left=self.left, right=self.right)
        else:
            elts = proc(elts)

        # d. formatting
        elts = components['frm'][self.frm](elts)

        return elts

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


class CheckFile(SpellCheck):
    def __init__(self, profile):
        SpellCheck.__init__(self, profile)

    def check_file(self, filename: str, out_folder: str = 'checked'):
        in_file = Path(filename)
        out_dir = Path(out_folder)
        assert in_file.is_file()
        out_dir.mkdir(exist_ok=True)
        out_file = out_dir / in_file.name

        with in_file.open(encoding='utf-8-sig') as f:
            dump = f.read()

        output = self.check(dump)

        with out_file.open('w', encoding='utf-8-sig') as g:
            g.write(output)
