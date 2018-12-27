from pathlib import Path
import csv
import re


def segment_with_tags(string, start_tag, end_tag, sep, in_tag_max=3):
    """segment a string on sep,
    yet keep everything between start and end tags in a single token.
    To avoid kilometric tokens, stop growing the token when sep has been encountered in_tag_max times.

    limitation: in case a token is truncated, it is left as is, without coming back and
    splitting it on the sep char.
    """
    chunks = []
    inside_tags = False
    chunk = ''
    sep_count = 0
    for char in string:
        if char == start_tag:
            inside_tags = True

        if inside_tags and char == sep:
            sep_count += 1

        if sep_count > in_tag_max:
            inside_tags = False
            sep_count = 0

        if inside_tags and char == end_tag:
            chunk += char
            chunks.append(chunk)
            chunk = ''
            inside_tags = False

        elif not inside_tags and char == sep:
            chunks.append(chunk)
            chunk = ''
            sep_count = 0

        else:
            chunk += char

    if chunk:
        chunks.append(chunk)

    return chunks


in_file = 'to-check/vernacular_list.csv'

dump = []
with open(in_file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    dump = list(spamreader)


for row in dump:
    for num, r in enumerate(row):
        r = r.replace('_', '')\
            .replace('\xa0', ' ')\
            .strip()\
            .replace('-', '')\
            .replace('$', '')\
            .strip()\
            .lstrip('་')
        row[num] = r

out = []
for row in dump:
    truc = row[1].strip().lstrip('་').strip()
    truc = re.sub(r'\s+', ' ', truc)
    chunks = segment_with_tags(truc, '[', ']', ' ')
    if not chunks:
        row[1] = truc
        continue
    chunks = [c.replace(' ', '')
                  .strip('[]')
                  .replace(']་', '་')
                  .replace(']', '')
                  .replace('[', '')
                  .replace('༜', '')
                  .replace('༼', '') for c in chunks]
    chunks = [c for c in chunks if c]
    truc = ' '.join(chunks)
    row[1] = truc.strip().replace(' ་', '་').replace('][', ' ')
    if row not in out:
        out.append(row)

okay = []
to_check = []
for r in out:
    if '[' in r[1] or ']' in r[1] or re.match(r'[0-9]', r[1]) or '༼' in r[1] or '༽' in r[1] or '༜' in r[1]:
        to_check.append(r)
    else:
        okay.append(r)

print('there is', len(to_check), 'bad entries.')
Path('bad_entries.csv').write_text('\n'.join([','.join(r) for r in to_check]))

Path('bospell/resources/vernacular.csv').write_text('\n'.join([','.join(r) for r in okay]))
print('ok')