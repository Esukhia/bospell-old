from pathlib import Path
from bospell import spellcheck


in_dir = 'to-check/corpus'
out_dir = 'checked/'

total = ''
in_files = Path(in_dir).glob('*.txt')
for f in in_files:
    print(f.name)
    with f.open(encoding='utf-8-sig') as g:
        dump = g.read()
        total += dump + '\n'

out = spellcheck(total,
                 preproc='corpus_vernacular',
                 tok='sgmt_corpus_vernacular',
                 proc='corpus_vernacular',
                 format='conc',
                 left=10,
                 right=10)


out_file = Path(out_dir) / 'total2.tsv'
with out_file.open('w', encoding='utf-8-sig') as h:
    h.write(out)
