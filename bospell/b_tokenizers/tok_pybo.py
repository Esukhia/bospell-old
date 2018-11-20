from pybo import BoTokenizer


def tok_pybo(string, profile):
    tok = BoTokenizer(profile)
    return tok.tokenize(string)
