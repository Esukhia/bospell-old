from typing import Tuple
import re


def left_context_size(idx: int, context: int) -> int:
    if idx - context < 0:
        return 0

    while idx - context < 0:
        context += 1
    return idx - context


def right_context_size(idx: int, context: int, maximum: int) -> int:
    while idx + context > maximum:
        context -= 1
    return idx + context


def find_context_sizes(idx: int, left: int, right: int, maximum: int) -> Tuple[int, int]:
    l_con = left_context_size(idx, left)
    r_con = right_context_size(idx, right, maximum)
    return l_con, r_con


def is_skrt(syl):
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
    """Uses is_skrt() to check for sanskrit syllables

    """
    skrt = False
    syls = word.strip('་').split('་')
    for s in syls:
        if is_skrt(s):
            skrt = True

    return skrt
