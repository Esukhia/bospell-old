from pathlib import Path

from bospell import CheckFile


in_dir = 'to-check/corpus'

out_dir = 'checked/cleaned_segmentation'
mode = 'corpus_seg_adjusted'
cf = CheckFile(mode)

out_dir2 = 'checked/corpus_types'
mode2 = 'corpus_stats_per_file'
cf2 = CheckFile(mode2)

for f in Path(in_dir).glob('*.*'):
    cf.check_file(f, out_dir)
    cf2.check_file(f, out_dir2)
