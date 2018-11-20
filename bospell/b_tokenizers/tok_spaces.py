
def basic(string):
    """Tokenizes string on "\n" and spaces

    :param string: to tokenize
    :return: list of tokens
    """
    string = string.replace('\n', ' ')
    return string.split(' ')
