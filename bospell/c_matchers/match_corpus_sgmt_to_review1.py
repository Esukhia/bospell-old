

def is_correction(token):
    return '༺' in token or '༻' in token


def is_to_merge(token):
    return token.startswith('༺') \
           and token.count('༺') == 1 \
           and token.endswith('༻') \
           and token.count('༻') == 1 \
           and ' ' in token


def find_to_review(tokens):
    to_review = {}
    for token in tokens:
        if is_to_merge(token):
            match = token[1:-1].split(' ')
            to_review[token] = match

    return to_review


def find_left_size(current, span):
    if current - span < 0:
        return 0

    while current - span < 0:
        span += 1
    return current - span


def find_right_size(current, span, max):
    while current + span > max:
        span -= 1
    return current + span


def corpus_sgmt_to_review(tokens, left=5, right=5):
    to_review = find_to_review(tokens)
    concs = []
    for orig, splitted in to_review.items():
        s = len(splitted)
        for i in range(len(tokens)):
            if tokens[i] == orig:
                l_size = find_left_size(i, left)
                r_size = find_right_size(i, right, len(tokens))
                conc = (tokens[l_size:i], tokens[i], tokens[i+1:r_size])
                concs.append(conc)
            elif tokens[i:i + s] == splitted:
                l_size = find_left_size(i, left)
                r_size = find_right_size(i + s, right, len(tokens))
                conc = (tokens[l_size:i], ' '.join(tokens[i:i + s]), tokens[i + 1:r_size])
                concs.append(conc)

    return concs
