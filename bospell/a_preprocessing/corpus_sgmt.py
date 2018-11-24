import re

VERNACULAR = ['༺', '༻']
CORRECTIONS = ['[', ']']
OTHERS = ['༼', '༽', '༜', '༙', '#', '$']


def corpus_cleanup(string):
    to_remove = VERNACULAR + OTHERS
    string = re.sub(r'༺(.+?)།.+?༻', r'\1', string)
    for t in to_remove:
        string = string.replace(t, '')
    string = re.sub(r'\s+', r' ', string)
    return string


def corpus_cleanup_vernacular(string):
    to_remove = CORRECTIONS + OTHERS
    string = re.sub(r'༺(.+?)།.+?༻', r'\1', string)
    for t in to_remove:
        string = string.replace(t, '')
    string = re.sub(r'\s+', r' ', string)
    return string


if __name__ == '__main__':
    test = 'ཨ །_༺ དུ་ར་ ༻༺ མི་ $ཧྲ་ ༻༺ མི་ ། ཧྲ་ ༻ གི་ ཡ །_༺ དུ་ ༻' \
           '༺ [ནང་][ང་] ། ནང་ན་ ༻ གཅིག་ ཐོན་ ཐལ་ ཡ ། ༺ [ནང་][ང་] ༻'
    result = corpus_cleanup(test)
    assert result == 'ཨ །_ དུ་ར་ མི་ ཧྲ་ མི་ གི་ ཡ །_ དུ་ [ནང་][ང་] གཅིག་ ཐོན་ ཐལ་ ཡ ། [ནང་][ང་] '
