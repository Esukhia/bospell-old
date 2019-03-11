from pathlib import Path
from collections import defaultdict

from bospell import *


in_path = Path('to-check/tengyur_last_volumes/')
out_path = Path('checked/tengyur_last_volumes/')
include_skrt = True

pipeline = BoPipeline(
            pipes['extract_tib_only'],
            'pybo',
            ('pybo_mistakes', pipes['find_mistake_types']),
            'dummy',
            pybo_profile='GMD'
        )

files = {
    in_path / 'lines - 170_འཁྲི་ཤིང།_ཀེ.csv': 'has_skrt',
    in_path / 'lines - 171_འཁྲི་ཤིང།_ཁེ.csv': 'has_skrt',
    in_path / 'lines - 202_གསོ་རིག_གོ.csv': '',
    in_path / 'lines - 203_སྣ་ཚོགས།_ངོ.csv': '',
    in_path / 'lines - 208_སྒྲ་མདོ།_ཏོ.csv': '',
    in_path / 'lines - 211_སྣ་ཚོགས།_ནོ.csv': '',
    in_path / 'lines - རྒྱུད་འགྲེལ། ནུ།.csv': '',
    in_path / 'lines - རྒྱུད་འགྲེལ། ཙི།.csv': ''
        }

mistakes = defaultdict(int)
for f, mode in files.items():
    content = f.read_text()
    if mode == 'has_skrt' and not include_skrt:
        pipeline = BoPipeline(
            pipes['extract_tib_only'],
            'pybo',
            'pybo_mistakes',
            'dummy',
            pybo_profile='GMD'
        )

        mistk = pipeline.pipe_str(content)
    else:
        pipeline = BoPipeline(
            pipes['extract_all'],
            'pybo',
            'pybo_mistakes',
            'dummy',
            pybo_profile='GMD'
        )

        mistk = pipeline.pipe_str(content)

    for m, freq in mistk.items():
        mistakes[m] += freq

m_types = sorted([(m, n) for m, n in mistakes.items()], key=lambda x: x[1], reverse=True)
m_types = [f'{t[0]},{t[1]}' for t in m_types]
Path('total_mistakes.csv').write_text('\n'.join(m_types))
