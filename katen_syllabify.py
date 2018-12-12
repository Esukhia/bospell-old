from pathlib import Path

from bospell import *

cf = CheckFile('syls')

for col in ['kangyur', 'tengyur']:
    for section in Path('to-check/' + col).glob('*'):
        for f in section.glob('*.*'):
            out_file = Path('checked/') / '/'.join(section.parts[1:]) / f.name
            for p in sorted(out_file.parents):
                if not p.is_dir():
                    p.mkdir(exist_ok=True)

            cf.check_file(f, out_file.parent)
