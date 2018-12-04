from pathlib import Path

from bospell import CheckFile


in_dir = 'to-check/corpus'
out_dir = 'checked/cleaned_segmentation'
mode = 'corpus_seg_adjusted'

cf = CheckFile(mode)

for f in Path(in_dir).glob('*.*'):
    dump = f.read_text()
    cf.check_file(f, out_dir)
