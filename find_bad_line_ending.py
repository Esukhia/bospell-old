from pathlib import Path


def extract_all(csv_dump):
    lines = csv_dump.strip().split('\n')  # cut dump in lines
    lines = [l.split(',')[1] for l in lines]  # only keep the text
    return lines


def has_bad_ending(line):
    if line and line.strip()[-1] not in '་།ཿ༔':
        return True
    return False


bad_lines = []
for f in Path('to-check/tengyur_last_volumes/').glob('*.csv'):
    lines = extract_all(f.read_text())
    for num, l in enumerate(lines):
        if has_bad_ending(l):
            line_end = '(...) ' + '་'.join(l.split('་')[-10:])
            bad_lines.append((f.stem, num, line_end))

out = '\n'.join([','.join([str(x) for x in a]) for a in bad_lines])
Path('bad_line_endings.csv').write_text(out)
