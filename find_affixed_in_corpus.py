import re
from pathlib import Path
from collections import defaultdict

files = Path('checked/cleaned_segmentation').glob('*.txt')

no_trailing_tsek = []
for f in files:
    content = f.read_text()
    name = f.stem.replace('_cleaned', '')
    types = defaultdict(int)

    matches = re.findall(r'(( |^|།)[^། ]+[^་།]) [^།]', content)
    matches = [a[0].strip() for a in matches]
    for m in matches:
        types[m] += 1

    no_trailing_tsek.append((name, types))

total_no_trailing = defaultdict(int)
for a, b in no_trailing_tsek:
    for k, v in b.items():
        total_no_trailing[k] += v

out = sorted([(k, v) for k, v in total_no_trailing.items()], reverse=True, key=lambda x: x[1])
Path('no_trailing_tsek_types.csv').write_text('\n'.join([','.join((str(a), str(b))) for a, b in out]))
print('ok')
