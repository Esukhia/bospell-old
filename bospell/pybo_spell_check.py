import re
import argparse
from pathlib import Path
from collections import defaultdict

import pybo


def is_sskrt(syl):
    """Source for regexes : Paul Hackett Visual Basic script

    regex1: Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
    regex2: more Sanskrit: invalid superscript-subscript pairs
    regex3: tsa-phru mark used in Chinese transliteration
    :param syl: syllable to assert
    :return: True if matches either of the regexes, False otherwise
    """
    regex1 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}" \
             r"[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}" \
             r"[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    return re.search(regex1, syl) or re.search(regex2, syl) or re.search(regex3, syl)


def is_skrt_word(word):
    is_skrt = False
    syls = word.strip('་').split('་')
    for s in syls:
        if is_sskrt(s):
            is_skrt = True
    return is_skrt


def is_mistake(token):
    exceptions = ['\n']
    if token.type == 'syl' or token.type == 'non-bo':
        if (not token.skrt
            and not is_skrt_word(token.cleaned_content)) \
           and \
            (token.pos == 'oov'
             or token.pos == 'non-word'
             or token.type == 'non-bo') \
           and token.content not in exceptions:
            return True
    return False


def find_mistake_concs(tokens, work_name, context=5):
    mistakes = defaultdict(list)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            if num - context < 0:
                left = tokens[:num]
            else:
                left = tokens[num - context:num]
            if num + context > len(tokens)-1:
                right = tokens[num+1:]
            else:
                right = tokens[num+1:num+1+context]

            left = [t.content for t in left]
            right = [t.content for t in right]
            mis = t.content.replace('\n', '\\n')
            mistakes[mis].append((work_name, [''.join(left), ''.join(right)]))
    return mistakes


def generate_mistake_concs(in_files):
    total = defaultdict(list)
    for f in in_files:
        print(f.stem)
        content = f.read_text(encoding='utf-8-sig')
        pybo_segmented = tok.tokenize(content)
        mistakes = find_mistake_concs(pybo_segmented, f.stem)
        for k, v in mistakes.items():
            total[k].extend(v)

    # sort by total frequency
    sorted_types = sorted(total, key=lambda x: len(total[x]), reverse=True)
    return total, sorted_types


def format_concs(total_mistakes, sorted_types, file=''):
    output = []
    for mis in sorted_types:
        mis = mis.replace('\n', '\\n')
        if '\n' in mis:
            print('ok')
        tmp = []
        for occ in total_mistakes[mis]:

            if file and file != occ[0]:
                continue

            left, right = occ[1][0], occ[1][1]
            conc = f"{''.join(left)}|– {mis} –|{''.join(right)}"
            conc = conc.replace('\n', '\\n')
            tmp.append(conc)

        if tmp:
            out = f'"{mis}" {len(tmp)}' + '\n\t' + '\n\t'.join(tmp) + '\n'
            output.append(out)
    return output


def find_total_types(total_mistakes, sep=''):
    total = []
    for t in total_mistakes:
        total.append((t, len(total_mistakes[t])))
    total = sorted(total, reverse=True, key=lambda x: x[1])
    total = [f'{t[0]}{sep}{t[1]}' for t in total]
    return total


def write_file_concs(total_mistakes, sorted_types, in_files, out_dir):
    out_path = out_dir / 'concs'
    out_path.mkdir(exist_ok=True)
    for f in in_files:
        output = format_concs(total_mistakes, sorted_types, f.stem)

        out_file = out_path / f'{f.stem}_segmented.txt'
        out_file.write_text('\n\n'.join(output), encoding='utf-8-sig')


def write_total_concs(total_mistakes, sorted_types, out_dir):
    concs = format_concs(total_mistakes, sorted_types)
    types = find_total_types(total_mistakes)
    out = ', '.join(types) + '\n\n' + '\n\n'.join(concs)
    Path(out_dir / 'total_mistakes.txt').write_text(out, encoding='utf-8-sig')


parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True, help='folder containing the files to check')
parser.add_argument('-o', required=True, help='folder to contain the output')
parser.add_argument('-c', help='generates a conc file for each input file if "true"')

if __name__ == '__main__':
    # args = parser.parse_args()

    in_dir = 'out'#args.i
    out_dir = 'segmented'#args.o
    gen_concs = False#bool(args.c)
    if not in_dir or not out_dir:
        parser.print_help()
        exit()

    pybo_mode = 'GMD'
    in_files = sorted(Path(in_dir).glob('*.txt'))
    out_dir = Path(out_dir)

    tok = pybo.BoTokenizer(pybo_mode)  # GMD includes all available wordlists + sanskrit

    concs, sorted_types = generate_mistake_concs(in_files)

    if gen_concs:
        write_file_concs(concs, sorted_types, in_files, out_dir)

    write_total_concs(concs, sorted_types, out_dir)

    types = find_total_types(concs, sep='\t')
    Path(out_dir / 'mistake_types.txt').write_text('\n'.join(types))
