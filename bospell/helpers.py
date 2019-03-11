import re


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
