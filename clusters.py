import re
from resources.pybo.pybo.pybo import *


class BasicTests:
    """
    This class contains the basic tests that will need to be aggregated into
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

    @staticmethod
    def is_punct_token(token):
        return token.tag == 'punct'

    @staticmethod
    def is_monosyl_token(token):
        return token.syls and len(token.syls) == 1

    def is_non_bo_token(self, token):
        return self.OTHER in token.char_groups.values()

    def is_non_word(self, token):
        return token.tag == self.NON_WORD

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


class MatcherTests(BasicTests):
    """
    This class builds on top of the single-purposed tests defined in BasicTests
    to build tests that will be usable in the real world.

    The declared here should only aggregate the tests in BasicTests into new methods
    They should not declare any concrete test.
    """
    def __init__(self):
        BasicTests.__init__(self)

    def mono_or_punct_or_nonword(self, token):
        return self.is_monosyl_token(token) or \
               self.is_punct_token(token) or \
               self.is_non_word(token)

    def skrt(self, token):
        return self.has_skrt_syl(token) or \
               self.has_skrt_char(token)


class TokenClusters:
    def __init__(self):
        self.tests = MatcherTests()

    @staticmethod
    def piped_clusterize(clusterized, condition):
        """
        Uses "condition" to decide if a given cluster should be kept or if it should
        be dismantled.
        A cluster is kept if at least one of its elements satisfies "condition".

        :param clusterized: a clusterized list of Token objects
        :param condition: function to test if cluster should be kept
        :return: modified clusterized
        """
        result = []
        for token_or_list in clusterized:
            if type(token_or_list) != list:
                result.append(token_or_list)
            else:  # assuming it is always a list
                passes = False
                for token in token_or_list:
                    if condition(token):
                        passes = True

                if passes:
                    result.append(token_or_list)
                else:
                    result.extend(token_or_list)
        return result

    @staticmethod
    def nonword_or_skrt_piped_clusterize(clusterized, skrt_condition, nonword_condition):
        """
        flags clusters with skrt as 'skrt', clusters with nonwords as 'nonword',
        dismantled the others.

        :param clusterized:
        :param condition:
        :return:
        """
        result = []
        for token_or_list in clusterized:
            if type(token_or_list) != list:
                result.append(token_or_list)
            else:  # assuming it is always a list
                conditions = []
                for token in token_or_list:
                    is_skrt = False
                    is_nonword = False
                    if skrt_condition(token):
                        is_skrt = True
                    if nonword_condition(token):
                        is_nonword = True

                    # if for the same token
                    if is_skrt and is_nonword:
                        conditions.append('s')
                    elif is_skrt:
                        conditions.append('s')
                    elif is_nonword:
                        conditions.append('n')

                if 's' in conditions and 'n' in conditions:
                    result.append({'both': token_or_list})
                elif 's' in conditions:
                    result.append({'skrt': token_or_list})
                elif 'n' in conditions:
                    result.append({'non-word': token_or_list})
                else:
                    result.extend(token_or_list)

        return result

    @staticmethod
    def clusterize(tokens, condition):
        """
        Creates clusters of tokens that satisfy the condition given as argument.

        :param tokens: a list of Token objects(output of pybo.Tokenizer)
        :param condition: function to test whether a token should be integrated into a cluster or not
        :return: tokens, but with all the tokens passing the test put into a list.
                thus, an element in the resulting list can either be a Token object or a list of Token objects.
        """
        clusters = []
        tmp = []
        for token in tokens:
            if condition(token):
                tmp.append(token)
            else:
                if tmp:
                    clusters.append(tmp)
                    tmp = []
                clusters.append(token)
        return clusters

    @staticmethod
    def format_single_syl_clusters(clusterized):
        """
        for every token, extract the raw content and add it to "out".
        for every cluster, extract the contents and join them with "-" and add double parens
        to visually identify them.

        :param clusterized: clusterized list of Token objects
        :return: the
        """
        out = ''
        for elt in clusterized:
            if type(elt) == list:
                out += '《{}》'.format('|'.join([token.content for token in elt]))
            else:
                out += elt.content
        return out

    @staticmethod
    def tokens_to_str(clusters):
        """
        returns the same clustered structure, but replaces Token objects with strings.
        :param clusters:
        :return:
        """
        str_structure = []
        for cl in clusters:
            if type(cl) != dict:
                str_structure.append(cl.content)
            else:
                key = list(cl.keys())[0]
                new = {key: []}
                for token in cl[key]:
                    new[key].append(token.content)
                str_structure.append(new)
        return str_structure


def tokens_from_string(to_tokenize, trie_profile='pytib'):
    """
    Generates tokens from a given input string

    :param to_tokenize: string to tokenize
    :param trie_profile: profile of PyBoTrie to pass on
    :return: a list of Token objects

    .. note:: is not optimized because it instanciates all the classes from
    pybo at every call
    """
    # a. instanciate the tokenizer
    bs = BoSyl()  # used to dynamically generate affixed versions
    trie = PyBoTrie(bs, profile=trie_profile)  # loads or builds a trie
    tok = Tokenizer(trie)

    # b. pre-process the input string
    pre_processed = PyBoTextChunks(to_tokenize)

    # c. tokenize
    tokens = tok.tokenize(pre_processed)
    return tokens


def str_clusters_from_string(in_str):
    """
    - Tokenizes the input string with pybo
    - Creates clusters containing mono-syllabled tokens, punctuation and non-words
    - filters the clusters to only keep those with skrt syls or non-word syls
    - converts from tokens to strings

    :param in_str: input string to be processed
    :return: a string representation of the created clusters
    """
    t = MatcherTests()
    cl = TokenClusters()
    tokens = tokens_from_string(in_str)

    unfiltered_clusters = cl.clusterize(tokens, t.mono_or_punct_or_nonword)
    clusters = cl.nonword_or_skrt_piped_clusterize(unfiltered_clusters, t.has_skrt_syl, t.is_non_word)
    cluster = cl.tokens_to_str(clusters)

    return cluster


class Cluster:
    def __init__(self, raw_clusters):
        self.freqs = {}
        self.__load_freqs()
        self.base_structure = []
        self.clusters = []
        self.__load_clusters(raw_clusters)
        self.freq_structure = []
        self.__load_freq_structure()

    def __load_freqs(self):
        with open('resources/total_freqs.txt', 'r') as f:
            content = f.readlines()
            for line in content:
                word, freq = line.split()
                self.freqs[word] = int(freq)

    def __load_clusters(self, raw_clusters):
        count = 0
        for elt in raw_clusters:
            if type(elt) != dict:  # assuming it is a string
                self.base_structure.append(elt)
                count += 1
            else:
                key = list(elt.keys())[0]
                cluster = []
                for token in elt[key]:
                    self.base_structure.append(token)
                    count += 1
                    cluster.append(count)
                self.clusters.append({key: cluster})

    def __load_freq_structure(self):
        for token in self.base_structure:
            if token in self.freqs.keys():
                self.freq_structure.append(self.freqs[token])
            else:
                self.freq_structure.append(-1)

    def is_low_freq(self, token_idx):
        return self.freq_structure[token_idx] <= 1000

    def is_high_freq(self, token_idx):
        return self.freq_structure[token_idx] >= 1000

    def adjust_clusters(self):
        for i in range(len(self.clusters)-1):
            # for each side, 1. prune high frequency tokens, extend low frequency
            key = list(self.clusters[i])[0]
            left_token = self.clusters[i][key][0]
            right_token = self.clusters[i][key][-1]

            # A. adjust left context
            if self.is_high_freq(left_token):
                while self.is_high_freq(left_token) and left_token <= right_token:
                    left_token += 1
            elif self.is_low_freq(left_token):
                if self.is_low_freq(left_token - 1):
                    left_token -= 1
            # else do nothing: we have no frequency to work with, so leaving the cluster as-is

            # C. flag high frequency clusters
            if left_token == right_token:
                self.clusters[i] = {'high_freq_cluster': self.clusters[i][key]}
                continue

            # B. adjust right context
            else:
                if self.is_high_freq(right_token):
                    while self.is_high_freq(right_token) and right_token >= left_token:
                        right_token -= 1
                elif self.is_low_freq(right_token):
                    if self.is_low_freq(right_token + 1):
                        left_token += 1

            # C. flag high frequency clusters
            if left_token == right_token:
                self.clusters[i] = {'high_freq_cluster': self.clusters[i][key]}
                continue

            if left_token != self.clusters[i][key][0] or right_token != self.clusters[i][key][-1]:
                new_cluster = {key: list(range(left_token, right_token))}
                self.clusters[i] = new_cluster

    def export_clusters(self):
        out = []
        current_token = 0
        for cluster in self.clusters:
            key = list(cluster)[0]
            while cluster[key][0] > current_token:
                out.append(self.base_structure[current_token])
                current_token += 1

            str_cluster = [self.base_structure[token] for token in cluster[key]]
            out.append({key: str_cluster})
            current_token = cluster[key][-1] + 1

        return out


def generate_combinations(clusters):
    """
    Does nothing if not a non-word cluster, but could do anything else
    :param clusters:
    :return:
    """
    cluster_combs = []
    for num, elt in enumerate(clusters):
        if type(elt) != dict:
            pass
        else:
            key = list(elt)[0]
            if key == 'non-word':
                cluster_str = ''.join(elt[key])
                preprocessed = PyBoTextChunks(cluster_str).serve_syls_to_trie()
                syls = []
                for p in preprocessed:
                    if p[0]:
                        syl = ''.join([cluster_str[idx] for idx in p[0]])
                        syls.append(syl)

                combinations = [' '.join(syls[0:i + 1]) for i in range(len(syls))]
                cluster_combs.append(combinations)
    return cluster_combs


if __name__ == '__main__':
    page = """[29a.1]རྨི་ལམ་ངན་པ་དང་། ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་དང་། བྱད་དང་རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་འགྱུར། གང་གིས་མཁས་པ་དག་ཁྲུས་བགྱིད་དུ་སྩལ་བའི་སྨན་དང་སྔགས་ནི་འདི་དག་སྟེ། ཤུ་དག་གིའུ་ཝང་འུ་སུ་དང་། །ཤ་མྱང་ཤ་མི་ཤི་རི་ཤ །དབང་
[29a.2]པོའི་ལག་དང་སྐལ་བ་ཆེ། །ཛྙ་མ་ཤིང་ཚ་ཨ་ག་རུ། །ཤི་རི་བེ་སྟ་སྲ་རྩི་དང་། །གུ་གུལ་ར་ས་ཤླ་ལ་ཀི། །རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་དང་། །ཙནྡན་དང་ནི་ལྡོང་རོས་དང་། །གི་ཝང་བཅས་དང་རུ་རྟ་དང་། །གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་དང་། །སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད། །ནཱ་ག་གེ་
[29a.3]སར་ཨུ་ཤི་ར། །འདི་དག་ཆ་ནི་མཉམ་བགྱིས་ནས། །སྐར་མ་རྒྱལ་ལ་བཏགས་པར་བགྱི། །ཕྱེ་མ་ལ་ནི་སྔགས་ཚིག་འདི། །ལན་བརྒྱ་མངོན་པར་གདབ་པར་བགྱི། །ཏད་ཡ་ཐཱ། སུ་ཀྲྀ་ཏེ་ཀྲྀ་ཏ་ཀ་མ་ལ་ནཱི་ལ་ཛི་ན་ཀ་ར་ཏེ། ཧཾ་ཀ་རཱ་ཏེ། ཨིནྡྲ་ཛ་ལི། ཤ་ཀད་དྲེ་བ་ཤད་དྲེ། ཨ་བརྟ་ཀ་
[29a.4]སི་ཀེ། ན་ཀུ་ཏྲ་ཀུ། ཀ་བི་ལ་ཀ་བི་ལ་མ་ཏི། ཤཱི་ལ་མ་ཏི། སན་དྷི་དྷུ་དྷུ་མ་མ་བ་ཏི། ཤི་རི་ཤི་རི། ས་ཏྱ་སྠི་ཏེ་སྭཱ་ཧཱ། ལྕི་བས་དཀྱིལ་འཁོར་བགྱིས་ནས་ནི། །མེ་ཏོག་སིལ་མ་དགྲམ་པར་བགྱི། །གསེར་གྱི་སྣོད་དང་དངུལ་སྣོད་དུ། །མངར་བའི་ཁུ་བ་གཞག་པར་བགྱི། །སྐྱེས་བུ་གོ་ཆ་བགོས་པ་ནི། །བཞི་ཞིག་དེར་
[29a.5]ཡང་གཞག་པར་བགྱི། །རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་བཞི། །བུམ་པ་ཐོགས་པ་གཞག་པར་བགྱི། །རྟག་ཏུ་གུ་གུལ་བདུག་པར་བགྱི། །སིལ་སྙན་སྣ་ལྔ་བགྱིད་དུ་སྩལ། །གདུགས་དང་རྒྱལ་མཚན་བ་དན་གྱིས། །ལྷ་མོ་དེ་ནི་ལེགས་པར་བརྒྱན། །བར་བར་དག་ཏུ་མེ་ལོང་གཞག །མདའ་དང་
[29a.6]མདུང་རྩེ་རྣ་བྲང་གཞག །དེ་ནས་མཚམས་ཀྱང་གཅད་པར་བགྱི། །དེ་ཡི་འོག་ཏུ་དགོས་པ་བརྩམ། །སྔགས་ཀྱི་ལས་ནི་འདི་དག་གིས། །མཚམས་བཅད་པ་ཡང་བརྩམ་པར་བགྱི། །སྱད་ཡ་ཐེ་དན། ཨ་ར་ཀེ །ན་ཡ་ནེ། ཧི་ལེ། མི་ལེ། གི་ལེ། ཁི་ཁི་ལེ་སྭཱ་ཧཱ། བཅོམ་
[29a.7]ལྡན་འདས་ཀྱི་སྣམ་ལོགས་སུ་ཁྲུས་བགྱིས་ནས་སྔགས་འདི་བཟླས་བརྗོད་བགྱིས་ན་ཁྲུས་ཀྱི་ཞི་བར་སྦྱོར་རོ། །ཏད་ཡ་ཐཱ། ས་ག་ཊེ། བི་ག་ཌེ། བི་ག་ཏ་བ་ཏི་སྭཱ་ཧཱ། ཕྱོགས་བཞི་དག་ན་གང་གནས་པའི། །རྒྱུ་སྐར་དག་གིས་ཚེ་སྲུངས་ཤིག །བཙས་པའི་སྐར་མའི་གནོད་པ་དང་། །"""
    clusters = str_clusters_from_string(page)
    cl_object = Cluster(clusters)
    before_adjusting = cl_object.export_clusters()
    cl_object.adjust_clusters()
    after_adjusting = cl_object.export_clusters()

    before_formatted = ''.join([cl if type(cl) == str else '《{}: {}》'.format(list(cl.keys())[0], '|'.join(cl[list(cl.keys())[0]])) for cl in before_adjusting])
    # print(clusters)
    print(before_formatted)
    # [29a.1]རྨི་ལམ་ངན་པ་དང་། ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་དང་། བྱད་དང་རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་འགྱུར། གང་གིས་མཁས་པ་དག་《non-word: ཁྲུས་|བགྱིད་|སྩལ་བའི་》སྨན་དང་སྔགས་ནི་འདི་དག་སྟེ། ཤུ་དག་གིའུ་《non-word: ཝང་|འུ་སུ་》དང་། །ཤ་མྱང་ཤ་མི་ཤི་རི་ཤ །དབང་
    # [29a.2]པོའི་ལག་དང་སྐལ་བ་ཆེ། །ཛྙ་མ་ཤིང་ཚ་ཨ་《non-word: ག་|རུ|། |།|ཤི་|རི་|བེ་|སྲ་རྩི་》དང་། །གུ་གུལ་ར་ས་ཤླ་ལ་ཀི། །རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་དང་《skrt: ། |།|ཙནྡན་|དང་|ནི་|ལྡོང་རོས་》དང་། །གི་ཝང་བཅས་དང་རུ་རྟ་དང་། །གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་དང་། །སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད། །ནཱ་ག་གེ་《non-word: སར་|ཨུ་|ར|། |།|འདི་དག་》ཆ་ནི་མཉམ་བགྱིས་ནས། །སྐར་མ་རྒྱལ་ལ་བཏགས་པར་བགྱི། །ཕྱེ་མ་ལ་ནི་སྔགས་ཚིག་འདི། །ལན་བརྒྱ་མངོན་པར་གདབ་པར་བགྱི《both: ། |།|ཏད་|ཡ་|ཐཱ|།| སུ་|ཀྲྀ་|ཏེ་|ཀྲྀ་|ཏ་|ཀ་མ་ལ་》ནཱི་《skrt: ལ་|ཛི་ན་》ཀ་ར་ཏེ《both: །| ཧཾ་|ཀ་|རཱ་|།| ཨིནྡྲ་|ཛ་|ལི|།| ཤ་|ཀད་|དྲེ་|བ་|ཤད་|དྲེ|།| ཨ་|བརྟ་|
    # [29a.4]》སི་《non-word: ཀེ|།| ན་|ཀུ་|ཀུ| ཀ་|བི་|ཀ་|བི་|མ་ཏི》།《skrt:  ཤཱི་|ལ་མ་》ཏི《both:  སན་|དྷི་|དྷུ་|དྷུ་|མ་མ་》བ་《both: ཏི| ཤི་|རི་|ཤི་|རི|།| ས་|ཏྱ་|སྠི་|ཏེ་|སྭཱ་|ཧཱ|།| ལྕི་བས་》དཀྱིལ་འཁོར་བགྱིས་ནས་ནི། །མེ་ཏོག་སིལ་མ་དགྲམ་པར་བགྱི། །གསེར་གྱི་སྣོད་དང་དངུལ་སྣོད་དུ། །མངར་བའི་ཁུ་བ་གཞག་པར་བགྱི། །སྐྱེས་བུ་གོ་ཆ་བགོས་པ་ནི། །བཞི་ཞིག་དེར་
    # [29a.5]ཡང་གཞག་པར་བགྱི། །རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་བཞི། །བུམ་པ་ཐོགས་པ་གཞག་པར་བགྱི། །རྟག་ཏུ་གུ་གུལ་བདུག་པར་བགྱི། །སིལ་སྙན་སྣ་《non-word: ལྔ་|བགྱིད་|སྩལ|། |།|གདུགས་|དང་|རྒྱལ་མཚན་》བ་དན་གྱིས། །ལྷ་མོ་དེ་ནི་ལེགས་པར་བརྒྱན། །བར་བར་དག་ཏུ་མེ་ལོང་གཞག །མདའ་དང་
    # [29a.6]མདུང་རྩེ་རྣ་བྲང་གཞག །དེ་ནས་མཚམས་ཀྱང་གཅད་པར་བགྱི། །དེ་ཡི་འོག་ཏུ་དགོས་པ་བརྩམ། །སྔགས་ཀྱི་ལས་ནི་འདི་དག་གིས། །མཚམས་བཅད་པ་ཡང་བརྩམ་པར་བགྱི《non-word: ། |།|སྱད་|ཡ་|ཐེ་|།| ཨ་ར་》ཀེ 《both: །|ན་|ཡ་|ནེ| ཧི་|ལེ|།| མི་|ལེ|།| གི་|ལེ|།| ཁི་|ལེ་|སྭཱ་|ཧཱ|།| བཅོམ་|
    # [29a.7]》ལྡན་འདས་ཀྱི་སྣམ་ལོགས་སུ་ཁྲུས་བགྱིས་ནས་སྔགས་འདི་བཟླས་བརྗོད་བགྱིས་ན་ཁྲུས་ཀྱི་ཞི་བར་སྦྱོར་《both: རོ|། |།|ཏད་|ཡ་|ཐཱ|།| ས་ག་》ཊེ《both: །| བི་|ཌེ|།| བི་|ཏ་|བ་|ཏི་|ཧཱ|།| ཕྱོགས་|བཞི་|དག་|ན་|གང་|གནས་པའི》
    print()

    after_formatted = ''.join(
        [cl if type(cl) == str else '《{}: {}》'.format(list(cl.keys())[0], '|'.join(cl[list(cl.keys())[0]])) for cl in
         after_adjusting])
    print(after_formatted)
    # [29a.1]རྨི་ལམ་ངན་པ་དང་། ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་དང་། བྱད་དང་རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་འགྱུར། གང་གིས་མཁས་པ་དག་《high_freq_cluster: ཁྲུས་|བགྱིད་|སྩལ་བའི་》སྨན་དང་སྔགས་ནི་འདི་དག་སྟེ། ཤུ་དག་《non-word: གིའུ་|ཝང་》འུ་སུ་དང་། །ཤ་མྱང་ཤ་མི་ཤི་རི་ཤ །དབང་
    # [29a.2]པོའི་ལག་དང་སྐལ་བ་ཆེ། །ཛྙ་མ་ཤིང་ཚ་ཨ་ག་རུ《non-word: ། |།|ཤི་|རི་|བེ་》སྲ་རྩི་དང་། །གུ་གུལ་ར་ས་ཤླ་ལ་ཀི། །རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་དང་《skrt: ། |།|ཙནྡན་|དང་|ནི་|ལྡོང་རོས་》དང་། །གི་ཝང་བཅས་དང་རུ་རྟ་དང་། །གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་དང་། །སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད། །ནཱ་ག་གེ་སར་《non-word: ཨུ་|ར|། |།》འདི་དག་ཆ་ནི་མཉམ་བགྱིས་ནས། །སྐར་མ་རྒྱལ་ལ་བཏགས་པར་བགྱི། །ཕྱེ་མ་ལ་ནི་སྔགས་ཚིག་འདི། །ལན་བརྒྱ་མངོན་པར་གདབ་པར་བགྱི《both: ། |།|ཏད་|ཡ་|ཐཱ|།| སུ་|ཀྲྀ་|ཏེ་|ཀྲྀ་|ཏ་|ཀ་མ་ལ་》ནཱི་《high_freq_cluster: ལ་|ཛི་ན་》ཀ་ར་ཏེ།《both:  ཧཾ་|ཀ་|རཱ་|།| ཨིནྡྲ་|ཛ་|ལི|།| ཤ་|ཀད་|དྲེ་|བ་|ཤད་|དྲེ|།| ཨ་|བརྟ་》
    # [29a.4]སི་ཀེ།《non-word:  ན་|ཀུ་|ཀུ| ཀ་|བི་|ཀ་|བི་》མ་ཏི།《skrt:  ཤཱི་|ལ་མ་》ཏི《both:  སན་|དྷི་|དྷུ་》དྷུ་མ་མ་བ་ཏི《both:  ཤི་|རི་|ཤི་|རི|།| ས་|ཏྱ་|སྠི་|ཏེ་|སྭཱ་|ཧཱ|།》 ལྕི་བས་དཀྱིལ་འཁོར་བགྱིས་ནས་ནི། །མེ་ཏོག་སིལ་མ་དགྲམ་པར་བགྱི། །གསེར་གྱི་སྣོད་དང་དངུལ་སྣོད་དུ། །མངར་བའི་ཁུ་བ་གཞག་པར་བགྱི། །སྐྱེས་བུ་གོ་ཆ་བགོས་པ་ནི། །བཞི་ཞིག་དེར་
    # [29a.5]ཡང་གཞག་པར་བགྱི། །རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་བཞི། །བུམ་པ་ཐོགས་པ་གཞག་པར་བགྱི། །རྟག་ཏུ་གུ་གུལ་བདུག་པར་བགྱི། །སིལ་སྙན་སྣ་《high_freq_cluster: ལྔ་|བགྱིད་|སྩལ|། |།|གདུགས་|དང་|རྒྱལ་མཚན་》བ་དན་གྱིས། །ལྷ་མོ་དེ་ནི་ལེགས་པར་བརྒྱན། །བར་བར་དག་ཏུ་མེ་ལོང་གཞག །མདའ་དང་
    # [29a.6]མདུང་རྩེ་རྣ་བྲང་གཞག །དེ་ནས་མཚམས་ཀྱང་གཅད་པར་བགྱི། །དེ་ཡི་འོག་ཏུ་དགོས་པ་བརྩམ། །སྔགས་ཀྱི་ལས་ནི་འདི་དག་གིས། །མཚམས་བཅད་པ་ཡང་བརྩམ་པར་བགྱི། 《non-word: །|སྱད་|ཡ་|ཐེ་|།》 ཨ་ར་ཀེ །ན་ཡ་《both: ནེ| ཧི་|ལེ|།| མི་|ལེ|།| གི་|ལེ|།| ཁི་|ལེ་|སྭཱ་|ཧཱ|།| བཅོམ་》
    # [29a.7]ལྡན་འདས་ཀྱི་སྣམ་ལོགས་སུ་ཁྲུས་བགྱིས་ནས་སྔགས་འདི་བཟླས་བརྗོད་བགྱིས་ན་ཁྲུས་ཀྱི་ཞི་བར་སྦྱོར་རོ། 《both: །|ཏད་|ཡ་|ཐཱ|།》 ས་ག་ཊེ《both: །| བི་|ཌེ|།| བི་|ཏ་|བ་|ཏི་|ཧཱ|།| ཕྱོགས་|བཞི་|དག་|ན་|གང་|གནས་པའི》
    print()

    # Generating combinations only keeping non-word clusters.
    combinations = generate_combinations(after_adjusting)
    print(combinations)
    # [['གིའུ', 'གིའུ ཝང'],
    # ['ཤི', 'ཤི རི', 'ཤི རི བེ'],
    # ['ཨུ', 'ཨུ ར'],
    # ['ན', 'ན ཀུ', 'ན ཀུ ཀུཀ', 'ན ཀུ ཀུཀ བི', 'ན ཀུ ཀུཀ བི ཀ', 'ན ཀུ ཀུཀ བི ཀ བི'],
    # ['སྱད', 'སྱད ཡ', 'སྱད ཡ ཐེ']]
