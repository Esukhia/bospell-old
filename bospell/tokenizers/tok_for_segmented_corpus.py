
def segmt_corpus(string):
    """Tokenizes string on "\n" and spaces

    :param string: to tokenize
    :return: list of tokens
    """
    string = string.replace('\n', ' ')
    string = string.replace('_', '_ ')  # so that spaces in orig string is used
    return string.split(' ')
