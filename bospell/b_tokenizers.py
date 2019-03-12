from pybo import BoTokenizer


profile = 'GMD'
tok = BoTokenizer(profile)  # instanciate the tok here so it won't be reloaded at each call


def custom_pybo_tok(text):
    return tok.tokenize(text)
