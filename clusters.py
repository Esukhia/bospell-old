from pybo import *

import re
import hashids

import ngram
import pickle

from symspellcompound.symspellcompound import SySpellCompound

class Tests:
    """
    This class contains the tests that will need to be aggregated into
    real testing functions.

    As soon we want to test something in a Token object, we should check if it is
    in this class or not, if not, include it.
    """
    def __init__(self):
        # extracted from BoString
        self.CONS = 1
        self.SUB_CONS = 2
        self.VOW = 3
        self.TSEK = 4
        self.SKRT_CONS = 5
        self.SKRT_SUB_CONS = 6
        self.SKRT_VOW = 7
        self.PUNCT = 8
        self.NUM = 9
        self.IN_SYL_MARK = 10
        self.SPECIAL_PUNCT = 11
        self.SYMBOLS = 12
        self.NON_BO_NON_SKRT = 13
        self.OTHER = 14
        self.SPACE = 15
        self.UNDERSCORE = 16
        # extracted from BoChunk
        self.BO_MARKER = 100
        self.NON_BO_MARKER = 101
        self.PUNCT_MARKER = 102
        self.NON_PUNCT_MARKER = 103
        self.SPACE_MARKER = 104
        self.NON_SPACE_MARKER = 105
        self.SYL_MARKER = 106
        # other attributes
        self.OOV = 'XXX'  # https://github.com/Esukhia/pybo/blob/master/pybo/BoTrie.py#L209
        self.SOAS_OOV = 'X'  # in pybo/resources/trie/Tibetan.DICT
        self.NON_WORD = 'non-word'  # pybo/BoTokenizer.py#L156
        self.LFM = 1000 # Hightest low frequency of the monosyllabic words

    @staticmethod
    def is_punct_token(token):
        return token.tag == 'punct'

    @staticmethod
    def is_monosyl_token(token):
        return token.syls and len(token.syls) == 1

    def is_non_bo_token(self, token):
        return self.OTHER in token.char_groups.values()

    def is_non_word_token(self, token):
        return token.tag == self.NON_WORD

    def is_skrt_token(self, token):
        return token.skrt

    def has_skrt_char(self, token):
        return self.SKRT_VOW in token.char_groups.values() or \
               self.SKRT_CONS in token.char_groups.values() or \
               self.SKRT_SUB_CONS in token.char_groups.values()

    def has_skrt_syl(self, token):
        """
        Generates the pre-processed syl str, then tests whether it is a
        Sanskrit syl.

        :param token: token to test
        :return: True if the token contains a Sanskrit syllable, False otherwise
        """
        has_skrt = False
        if token.syls:
            for syl in token.syls:
                clean_syl = ''.join([token.content[s] for s in syl])
                if self._is_skrt_syl(clean_syl):
                    has_skrt = True
        return has_skrt

    def _is_skrt_syl(self, syl):
        """
        Checks whether a given syllable is Sanskrit.
        Uses the regexes of Paul Hackett from his Visual Basic script

        :param syl: syllable to test
        :return: True if it is Sanskrit, False otherwise

        .. note:: the original comments are preserved
        .. Todo:: find source
        """
        # Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
        regex1 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|" \
                 r"[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|" \
                 r"[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
        # more Sanskrit: invalid superscript-subscript pairs
        regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
        # tsa-phru mark used in Chinese transliteration
        regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"

        return re.search(regex1, syl) or re.search(regex2, syl) or re.search(regex3, syl)

    def mono_or_punct_or_nonword(self, token):
        return self.is_monosyl_token(token) or self.is_punct_token(token) or self.is_non_word_token(token)

    def skrt(self, token):
        return self.has_skrt_syl(token) or self.has_skrt_char(token)

    def is_HFM(self, token):
        return token.freq > self.LFM

    def is_LFM(self, token):
        return token.freq <= self.LFM


class Structure:
    def __init__(self, page):
        self.clusters = []
        self.hash_clusters = []
        self.page = page



        self.tokens = self.tokenize()
        # a supprimer quand implémenté à Pybo
        self.freqs = {}
        self.freq_tokens()
        self.skrt_tokens()

        self.clusterize()
        self.adjust_clusters()
        self.cluster_format()

    def tokenize(self):
        tok = BoTokenizer("POS")
        return tok.tokenize(self.page)

    def freq_tokens(self):
        with open('resources/total_freqs.txt', 'r', encoding="utf8") as f:
            content = f.readlines()
            for line in content:
                word, freq = line.split()
                self.freqs[word] = int(freq)

        for token in self.tokens:
            if token.cleaned_content in self.freqs.keys():
                setattr(token, "freq", self.freqs[token.cleaned_content])

    def skrt_tokens(self):
        for token in self.tokens:
            setattr(token, "skrt", False)
            if test.is_monosyl_token(token) and test.skrt(token):
                token.skrt = True

    def clusterize(self):
        tmp = []
        for i, token in enumerate(self.tokens):
            if test.mono_or_punct_or_nonword(token):
                if not (not tmp and test.is_punct_token(token)):
                    tmp.append(i)
            elif tmp:
                self.clusters.append([tmp[0], tmp[-1]])
                tmp = []

    def adjust_clusters(self):
        for i, cluster in enumerate(self.clusters):
            left_cluster_id = cluster[0]
            right_cluster_id = cluster[1]

            # Left context
            while left_cluster_id < right_cluster_id:
                if self.get_mono_token_freq(left_cluster_id) > test.LFM:
                    left_cluster_id += 1
                    while test.is_punct_token(self.tokens[left_cluster_id]):
                        left_cluster_id += 1
                else: break

            if left_cluster_id == right_cluster_id:
                if self.get_mono_token_freq(left_cluster_id) > test.LFM:
                    self.clusters[i] = None
                    continue
                else:
                    self.clusters[i] = [left_cluster_id]
                    continue
            elif left_cluster_id > right_cluster_id:
                self.clusters[i] = None
                continue
            else:
                cluster[0] = left_cluster_id

            # Right context
            while right_cluster_id > left_cluster_id:
                while test.is_punct_token(self.tokens[right_cluster_id]):
                    right_cluster_id -= 1
                if self.get_mono_token_freq(right_cluster_id) > test.LFM:
                    right_cluster_id -= 1
                else: break

            if right_cluster_id == left_cluster_id:
                if self.get_mono_token_freq(right_cluster_id) > test.LFM:
                    self.clusters[i] = None
                    continue
                else:
                    self.clusters[i] =  [right_cluster_id]
                    continue
            elif right_cluster_id < left_cluster_id:
                self.clusters[i] = None
                continue
            else:
                cluster[1] = right_cluster_id

        self.clusters = [c for c in self.clusters if c]

    def cluster_format(self):
        hash = hashids.Hashids(salt=hex(id(self)), min_length=9)
        for i, cluster_index in enumerate(self.clusters):
            type = self.cluster_type(cluster_index)
            hash_id = hash.encode(cluster_index[0])
            if len(cluster_index) == 1:
                self.clusters[i] = [hash_id, cluster_index[0], type]
            else:
                self.clusters[i] = [hash_id, tuple(cluster_index), type]
            self.hash_list = [hash_id]

        self.clusters = {k[0]: [k[1], k[2]] for k in self.clusters}

    def cluster_type(self, cluster_index):
        type = []
        if len(cluster_index) > 1:
            cluster_token = self.tokens[cluster_index[0]:cluster_index[1]+1]
        else:
            cluster_token = [self.tokens[cluster_index[0]]]

        while cluster_token:
            t = cluster_token.pop()
            if test.is_skrt_token(t):
                type.append("skrt")
            elif test.is_non_word_token(t):
                type.append(test.NON_WORD)
            elif test.is_monosyl_token(t):
                type.append("mono")

        if all([True if t == "skrt" else False for t in type]):
            return "skrt"
        elif any([True if t == "skrt" else False for t in type]):
            return "both"
        elif any([True if t == test.NON_WORD else False for t in type]):
            return test.NON_WORD
        elif all([True if t == "mono" else False for t in type]):
            return "mono"

    def get_mono_token_freq(self, index):
        if test.is_monosyl_token(self.tokens[index]):
            return self.tokens[index].freq



class Prediction:
    def __init__(self, clusters, tokens):
        self.clusters = clusters
        self.tokens = tokens
        self.limit=-1
        self.result = {}
        build = True
        rawPath = 'entries.txt'
        ngramPath = "ngram.pickled"

        if build or not os.path.isfile("ngram.pickled"):
            with open(rawPath, mode='r', encoding='utf-8') as f:
                G = ngram.NGram(f.read().splitlines(), N=2)
            pickle.dump(G, open(ngramPath, "wb"), -1)

        self.N = pickle.load(open(ngramPath, "rb"))

    def load_tokens(self, last_token=""):
        if not last_token:
                if self.right - self.left > 5:
                    for i, c in enumerate(self.tokens[self.left:self.right+1][0:5]):
                        if test.is_punct_token(c):
                            self.limit = i
                            tmp = self.tokens[self.left:self.right+1][0:i]
                            self.left = self.limit+1
                            while test.is_punct_token(self.tokens[self.left]):
                                self.left += 1
                            return tmp
                    else:
                        tmp = self.tokens[self.left:self.right+1][0:5]
                        self.left += 4
                        return tmp
                elif self.right - self.left < 0:
                    return -1
                else:
                    tmp = self.tokens[self.left:self.right+1]
                    self.left = self.right + 1
                    return tmp

    def ngrams(self):
        for k, v in self.clusters.items():
            if isinstance(v[0], tuple):
                self.left = v[0][0]
                self.right = v[0][1]
            else:
                self.left = self.right = v[0]


                self.left = self.get_previous_token(self.left)
                self.right = self.get_next_token(self.right)


            while True:
                self.cluster_tokens = []
                self.cluster_tokens = self.load_tokens()
                if self.cluster_tokens == -1: break


                for i in range(len(self.cluster_tokens)):
                    c = "".join([c.cleaned_content for c in self.cluster_tokens])
                    ngram_result = self.N.search(c, threshold=0.52)
                    if ngram_result: self.result[c] = ngram_result
                    self.cluster_tokens.pop()
                    if len(self.cluster_tokens) == 1 and test.is_HFM(self.cluster_tokens[0]): break

            print(self.result)

        print(self.N.search("ཆོ་ཉིད་", threshold=0.52))

    def get_previous_token(self, index):
        if index > 0 and not test.is_punct_token(self.tokens[index-1]):
            return index-1
        else: return index

    def get_next_token(self, index):
        if index < len(self.tokens) and not test.is_punct_token(self.tokens[index+1]):
            return index+1
        else: return index

    def symspell(self):
        ssc = SySpellCompound()
        ssc = SySpellCompound(maxDictionaryEditDistance=5)

        print(ssc.load_dictionary("lists/dictionary_bo_107_064.txt", term_index=0, count_index=1))
        print(ssc.lookup_compound(input_string="བཀྲ་ཤས་བདེ་ལགས་", edit_distance_max=2))



if __name__ == '__main__':

    page = '''ཁ་བཅོམ་འདན་འདས་དཔལ་ཀུན་ཏུ་བཟང་པོ་ལ་ཕྱག་འཚལ་ལོ།
     །རྒྱུད་གསུམ་ངེས་པར་བཤད་པ། དེ་ནས་དེའི་ཚེ་དེའི་དུས་ན་ཆོ་ཉིད་ཀྱི་མཁའ་དབྱངས་ཉིད་ཀྱི་ཀོང་།
      སེམས་ཉིད་ཀྱི་གནས་དེར་བྱང་ཆུབ་ཀྱི་སེམས་ཀུན་བྱེད་རྒྱལ་པོ་ཉིད་ཆོས་ཐམས་ཆེད་སྐྱེ་བ་མེད་པའི་ངང་ལ་དགོངས་ནས་སོགས་་་'''

    test = Tests()

    s = Structure(page)
    
    for t in s.tokens:
        if test.is_monosyl_token(t):
            print("TOKEN: %s content: %s tag: %s skrt: %s freq: %s" % (s.tokens.index(t), t.cleaned_content, t.tag, t.skrt, t.freq))
    print(s.clusters)
    p = Prediction(s.clusters, s.tokens)
    p.ngrams()
    p.symspell()
