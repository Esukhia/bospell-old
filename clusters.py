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

    @staticmethod
    def is_punct_token(token):
        return token.tag == 'punct'

    @staticmethod
    def is_monosyl_token(token):
        return token.syls and len(token.syls) == 1

    # not sure about the test. To check.
    @staticmethod
    def is_non_bo_token(token):
        return token.tag == 'OTHER'

    def has_skrt_char(self, token):
        return self.SKRT_VOW in token.char_groups.values() or \
               self.SKRT_CONS in token.char_groups.values() or \
               self.SKRT_SUB_CONS in token.char_groups.values()


class MatcherTests(BasicTests):
    """
    This class builds on top of the single-purposed tests defined in BasicTests
    to build tests that will be usable in the real world.

    The declared here should only aggregate the tests in BasicTests into new methods
    They should not declare any concrete test.
    """
    def __init__(self):
        BasicTests.__init__(self)

    def mono_or_punct(self, token):
        return self.is_monosyl_token(token) or \
               self.is_punct_token(token)


class TokenClusters:
    def __init__(self):
        self.tests = MatcherTests()

    def piped_clusterize(self, clusterized, condition):
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

    def clusterize(self, tokens, condition):
        """
        Creates clusters of tokens that satisfy the condition given as argument.
        Clusters with a single element are not considered clusters.

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
                    if len(tmp) == 1:
                        clusters.append(tmp[0])
                    else:
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
                out += '(({}))'.format('-'.join([token.content for token in elt]))
            else:
                out += elt.content
        return out


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


if __name__ == '__main__':
    page = """[29a.1]རྨི་ལམ་ངན་པ་དང་། ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་དང་། བྱད་དང་རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་འགྱུར། གང་གིས་མཁས་པ་དག་ཁྲུས་བགྱིད་དུ་སྩལ་བའི་སྨན་དང་སྔགས་ནི་འདི་དག་སྟེ། ཤུ་དག་གིའུ་ཝང་འུ་སུ་དང་། །ཤ་མྱང་ཤ་མི་ཤི་རི་ཤ །དབང་
[29a.2]པོའི་ལག་དང་སྐལ་བ་ཆེ། །ཛྙ་མ་ཤིང་ཚ་ཨ་ག་རུ། །ཤི་རི་བེ་སྟ་སྲ་རྩི་དང་། །གུ་གུལ་ར་ས་ཤླ་ལ་ཀི། །རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་དང་། །ཙནྡན་དང་ནི་ལྡོང་རོས་དང་། །གི་ཝང་བཅས་དང་རུ་རྟ་དང་། །གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་དང་། །སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད། །ནཱ་ག་གེ་
[29a.3]སར་ཨུ་ཤི་ར། །འདི་དག་ཆ་ནི་མཉམ་བགྱིས་ནས། །སྐར་མ་རྒྱལ་ལ་བཏགས་པར་བགྱི། །ཕྱེ་མ་ལ་ནི་སྔགས་ཚིག་འདི། །ལན་བརྒྱ་མངོན་པར་གདབ་པར་བགྱི། །ཏད་ཡ་ཐཱ། སུ་ཀྲྀ་ཏེ་ཀྲྀ་ཏ་ཀ་མ་ལ་ནཱི་ལ་ཛི་ན་ཀ་ར་ཏེ། ཧཾ་ཀ་རཱ་ཏེ། ཨིནྡྲ་ཛ་ལི། ཤ་ཀད་དྲེ་བ་ཤད་དྲེ། ཨ་བརྟ་ཀ་
[29a.4]སི་ཀེ། ན་ཀུ་ཏྲ་ཀུ། ཀ་བི་ལ་ཀ་བི་ལ་མ་ཏི། ཤཱི་ལ་མ་ཏི། སན་དྷི་དྷུ་དྷུ་མ་མ་བ་ཏི། ཤི་རི་ཤི་རི། ས་ཏྱ་སྠི་ཏེ་སྭཱ་ཧཱ། ལྕི་བས་དཀྱིལ་འཁོར་བགྱིས་ནས་ནི། །མེ་ཏོག་སིལ་མ་དགྲམ་པར་བགྱི། །གསེར་གྱི་སྣོད་དང་དངུལ་སྣོད་དུ། །མངར་བའི་ཁུ་བ་གཞག་པར་བགྱི། །སྐྱེས་བུ་གོ་ཆ་བགོས་པ་ནི། །བཞི་ཞིག་དེར་
[29a.5]ཡང་གཞག་པར་བགྱི། །རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་བཞི། །བུམ་པ་ཐོགས་པ་གཞག་པར་བགྱི། །རྟག་ཏུ་གུ་གུལ་བདུག་པར་བགྱི། །སིལ་སྙན་སྣ་ལྔ་བགྱིད་དུ་སྩལ། །གདུགས་དང་རྒྱལ་མཚན་བ་དན་གྱིས། །ལྷ་མོ་དེ་ནི་ལེགས་པར་བརྒྱན། །བར་བར་དག་ཏུ་མེ་ལོང་གཞག །མདའ་དང་
[29a.6]མདུང་རྩེ་རྣ་བྲང་གཞག །དེ་ནས་མཚམས་ཀྱང་གཅད་པར་བགྱི། །དེ་ཡི་འོག་ཏུ་དགོས་པ་བརྩམ། །སྔགས་ཀྱི་ལས་ནི་འདི་དག་གིས། །མཚམས་བཅད་པ་ཡང་བརྩམ་པར་བགྱི། །སྱད་ཡ་ཐེ་དན། ཨ་ར་ཀེ །ན་ཡ་ནེ། ཧི་ལེ། མི་ལེ། གི་ལེ། ཁི་ཁི་ལེ་སྭཱ་ཧཱ། བཅོམ་
[29a.7]ལྡན་འདས་ཀྱི་སྣམ་ལོགས་སུ་ཁྲུས་བགྱིས་ནས་སྔགས་འདི་བཟླས་བརྗོད་བགྱིས་ན་ཁྲུས་ཀྱི་ཞི་བར་སྦྱོར་རོ། །ཏད་ཡ་ཐཱ། ས་ག་ཊེ། བི་ག་ཌེ། བི་ག་ཏ་བ་ཏི་སྭཱ་ཧཱ། ཕྱོགས་བཞི་དག་ན་གང་གནས་པའི། །རྒྱུ་སྐར་དག་གིས་ཚེ་སྲུངས་ཤིག །བཙས་པའི་སྐར་མའི་གནོད་པ་དང་། །"""
    t = MatcherTests()
    cl = TokenClusters()

    tokens = tokens_from_string(page)

    mono_or_punct = cl.clusterize(tokens, t.mono_or_punct)
    mono_or_punct_with_skrt = cl.piped_clusterize(mono_or_punct, t.has_skrt_char)

    print(cl.format_single_syl_clusters(mono_or_punct))
    # [29a.1]རྨི་ལམ་ངན་པ་((དང་-།)) ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་((དང་-།- བྱད་-དང་))རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་((འགྱུར-།- གང་-གིས་))མཁས་པ་((དག་-ཁྲུས་-བགྱིད་))སྩལ་བའི་((སྨན་-དང་-སྔགས་-ནི་))འདི་དག་((སྟེ-།)) ཤུ་དག་((གིའུ་-ཝང་))འུ་སུ་((དང་-། -།-ཤ་-མྱང་-ཤ་-མི་-ཤི་-རི་-ཤ -།-དབང་))
    # [29a.2]((པོའི་-ལག་-དང་))སྐལ་བ་((ཆེ-། -།))ཛྙ་མ་ཤིང་ཚ་((ཨ་-ག་-རུ-། -།-ཤི་-རི་-བེ་))སྲ་རྩི་((དང་-། -།))གུ་གུལ་ར་ས་ཤླ་ལ་((ཀི-། -།))རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་((དང་-། -།-ཙནྡན་-དང་-ནི་))ལྡོང་རོས་((དང་-། -།))གི་ཝང་བཅས་དང་རུ་((རྟ་-དང་-། -།))གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་((དང་-། -།))སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད((། -།))ནཱ་ག་((གེ་-སར་-ཨུ་-ར-། -།))འདི་དག་((ཆ་-ནི་-མཉམ་-བགྱིས་-ནས-། -།))སྐར་མ་རྒྱལ་ལ་བཏགས་((པར་-བགྱི-། -།))ཕྱེ་མ་((ལ་-ནི་-སྔགས་-ཚིག་-འདི-། -།-ལན་-བརྒྱ་))མངོན་པར་གདབ་པར་((བགྱི-། -།-ཏད་-ཡ་-ཐཱ-།- སུ་-ཀྲྀ་-ཏེ་-ཀྲྀ་-ཏ་))ཀ་མ་ལ་((ནཱི་-ལ་))ཛི་ན་ཀ་ར་((ཏེ-།- ཧཾ་-ཀ་-རཱ་-།- ཨིནྡྲ་-ཛ་-ལི-།- ཤ་-ཀད་-དྲེ་-བ་-ཤད་-དྲེ-།- ཨ་-བརྟ་))
    # [29a.4]((སི་-ཀེ-།- ན་-ཀུ་-ཀུ- ཀ་-བི་-ཀ་-བི་))མ་ཏི((།- ཤཱི་))ལ་མ་((ཏི- སན་-དྷི་-དྷུ་-དྷུ་))མ་མ་((བ་-ཏི- ཤི་-རི་-ཤི་-རི-།- ས་-ཏྱ་-སྠི་-ཏེ་-སྭཱ་-ཧཱ-།)) ལྕི་བས་དཀྱིལ་འཁོར་((བགྱིས་-ནས་-ནི-། -།))མེ་ཏོག་སིལ་མ་དགྲམ་པར་((བགྱི-། -།-གསེར་-གྱི་-སྣོད་-དང་-དངུལ་-སྣོད་-དུ-། -།-མངར་-བའི་))ཁུ་བ་((གཞག་-པར་-བགྱི-། -།))སྐྱེས་བུ་གོ་ཆ་བགོས་པ་((ནི-། -།-བཞི་-ཞིག་-དེར་))
    # [29a.5]((ཡང་-གཞག་-པར་-བགྱི-། -།))རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་((བཞི-། -།))བུམ་པ་ཐོགས་པ་((གཞག་-པར་-བགྱི-། -།-རྟག་-ཏུ་))གུ་གུལ་((བདུག་-པར་-བགྱི-། -།))སིལ་སྙན་((སྣ་-ལྔ་-བགྱིད་-སྩལ-། -།-གདུགས་-དང་))རྒྱལ་མཚན་བ་དན་((གྱིས-། -།))ལྷ་མོ་((དེ་-ནི་))ལེགས་པར་((བརྒྱན-། -།))བར་བར་((དག་-ཏུ་))མེ་ལོང་((གཞག -།-མདའ་-དང་))
    # [29a.6]མདུང་རྩེ་((རྣ་-བྲང་-གཞག -།))དེ་ནས་((མཚམས་-ཀྱང་))གཅད་པར་((བགྱི-། -།-དེ་-ཡི་-འོག་-ཏུ་))དགོས་པ་((བརྩམ-། -།-སྔགས་-ཀྱི་-ལས་-ནི་))འདི་དག་((གིས-། -།-མཚམས་))བཅད་པ་ཡང་བརྩམ་པར་((བགྱི-། -།-སྱད་-ཡ་-ཐེ་-།)) ཨ་ར་((ཀེ -།-ན་-ཡ་-ནེ- ཧི་-ལེ-།- མི་-ལེ-།- གི་-ལེ-།- ཁི་-ལེ་-སྭཱ་-ཧཱ-།- བཅོམ་))
    # [29a.7]((ལྡན་-འདས་-ཀྱི་))སྣམ་ལོགས་((སུ་-ཁྲུས་-བགྱིས་-ནས་-སྔགས་-འདི་))བཟླས་བརྗོད་((བགྱིས་-ན་-ཁྲུས་-ཀྱི་))ཞི་བར་((སྦྱོར་-རོ-། -།-ཏད་-ཡ་-ཐཱ-།)) ས་ག་((ཊེ-།- བི་-ཌེ-།- བི་-ཏ་-བ་-ཏི་-ཧཱ-།- ཕྱོགས་-བཞི་-དག་-ན་-གང་))གནས་པའི((། -།))རྒྱུ་སྐར་((དག་-གིས་-ཚེ་-སྲུངས་-ཤིག -།))བཙས་པའི་སྐར་མའི་གནོད་པ་
    # Process finished with exit code 0
    print()

    print(cl.format_single_syl_clusters(mono_or_punct_with_skrt))
    # [29a.1]རྨི་ལམ་ངན་པ་དང་། ལོག་འདྲེན་གྱི་གནོད་པ་ཐམས་ཅད་དང་། བྱད་དང་རོ་ལངས་ཐམས་ཅད་རབ་ཏུ་ཞི་བར་འགྱུར། གང་གིས་མཁས་པ་དག་ཁྲུས་བགྱིད་སྩལ་བའི་སྨན་དང་སྔགས་ནི་འདི་དག་སྟེ། ཤུ་དག་གིའུ་ཝང་འུ་སུ་དང་། །ཤ་མྱང་ཤ་མི་ཤི་རི་ཤ །དབང་
    # [29a.2]པོའི་ལག་དང་སྐལ་བ་ཆེ། །ཛྙ་མ་ཤིང་ཚ་ཨ་ག་རུ། །ཤི་རི་བེ་སྲ་རྩི་དང་། །གུ་གུལ་ར་ས་ཤླ་ལ་ཀི། །རྡོ་དྲེག་ལོ་མ་རྒྱ་སྤོས་དང་། །ཙནྡན་དང་ནི་ལྡོང་རོས་དང་། །གི་ཝང་བཅས་དང་རུ་རྟ་དང་། །གུར་གུམ་གླ་སྒང་ཡུངས་ཀར་དང་། །སྦྱི་མོ་སུག་སྨེལ་ན་ལ་ད། །ནཱ་ག་གེ་སར་ཨུ་ར། །འདི་དག་ཆ་ནི་མཉམ་བགྱིས་ནས། །སྐར་མ་རྒྱལ་ལ་བཏགས་པར་བགྱི། །ཕྱེ་མ་ལ་ནི་སྔགས་ཚིག་འདི། །ལན་བརྒྱ་མངོན་པར་གདབ་པར་((བགྱི-། -།-ཏད་-ཡ་-ཐཱ-།- སུ་-ཀྲྀ་-ཏེ་-ཀྲྀ་-ཏ་))ཀ་མ་ལ་((ནཱི་-ལ་))ཛི་ན་ཀ་ར་((ཏེ-།- ཧཾ་-ཀ་-རཱ་-།- ཨིནྡྲ་-ཛ་-ལི-།- ཤ་-ཀད་-དྲེ་-བ་-ཤད་-དྲེ-།- ཨ་-བརྟ་))
    # [29a.4]སི་ཀེ། ན་ཀུ་ཀུ ཀ་བི་ཀ་བི་མ་ཏི((།- ཤཱི་))ལ་མ་ཏི སན་དྷི་དྷུ་དྷུ་མ་མ་((བ་-ཏི- ཤི་-རི་-ཤི་-རི-།- ས་-ཏྱ་-སྠི་-ཏེ་-སྭཱ་-ཧཱ-།)) ལྕི་བས་དཀྱིལ་འཁོར་བགྱིས་ནས་ནི། །མེ་ཏོག་སིལ་མ་དགྲམ་པར་བགྱི། །གསེར་གྱི་སྣོད་དང་དངུལ་སྣོད་དུ། །མངར་བའི་ཁུ་བ་གཞག་པར་བགྱི། །སྐྱེས་བུ་གོ་ཆ་བགོས་པ་ནི། །བཞི་ཞིག་དེར་
    # [29a.5]ཡང་གཞག་པར་བགྱི། །རབ་ཏུ་བརྒྱན་པའི་བུ་མོ་བཞི། །བུམ་པ་ཐོགས་པ་གཞག་པར་བགྱི། །རྟག་ཏུ་གུ་གུལ་བདུག་པར་བགྱི། །སིལ་སྙན་སྣ་ལྔ་བགྱིད་སྩལ། །གདུགས་དང་རྒྱལ་མཚན་བ་དན་གྱིས། །ལྷ་མོ་དེ་ནི་ལེགས་པར་བརྒྱན། །བར་བར་དག་ཏུ་མེ་ལོང་གཞག །མདའ་དང་
    # [29a.6]མདུང་རྩེ་རྣ་བྲང་གཞག །དེ་ནས་མཚམས་ཀྱང་གཅད་པར་བགྱི། །དེ་ཡི་འོག་ཏུ་དགོས་པ་བརྩམ། །སྔགས་ཀྱི་ལས་ནི་འདི་དག་གིས། །མཚམས་བཅད་པ་ཡང་བརྩམ་པར་བགྱི། །སྱད་ཡ་ཐེ་། ཨ་ར་((ཀེ -།-ན་-ཡ་-ནེ- ཧི་-ལེ-།- མི་-ལེ-།- གི་-ལེ-།- ཁི་-ལེ་-སྭཱ་-ཧཱ-།- བཅོམ་))
    # [29a.7]ལྡན་འདས་ཀྱི་སྣམ་ལོགས་སུ་ཁྲུས་བགྱིས་ནས་སྔགས་འདི་བཟླས་བརྗོད་བགྱིས་ན་ཁྲུས་ཀྱི་ཞི་བར་((སྦྱོར་-རོ-། -།-ཏད་-ཡ་-ཐཱ-།)) ས་ག་((ཊེ-།- བི་-ཌེ-།- བི་-ཏ་-བ་-ཏི་-ཧཱ-།- ཕྱོགས་-བཞི་-དག་-ན་-གང་))གནས་པའི། །རྒྱུ་སྐར་དག་གིས་ཚེ་སྲུངས་ཤིག །བཙས་པའི་སྐར་མའི་གནོད་པ་