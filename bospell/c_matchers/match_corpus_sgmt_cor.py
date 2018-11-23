

def is_correction(token):
    return '༺' in token or '༻' in token


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


def corpus_sgmt_cor(tokens, left=5, right=5):
    concs = []
    for i in range(len(tokens)):
        token = tokens[i]
        if is_correction(token):
            l_size = find_left_size(i, left)
            r_size = find_right_size(i, right, len(tokens))
            conc = (tokens[l_size:i], token, tokens[i+1:r_size])
            concs.append(conc)

    return concs
