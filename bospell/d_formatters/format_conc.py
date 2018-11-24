
def escape(string):
    # if '\t' in string or '\n' in string or ',' in string:
        return '"' + string + '"'
    # return string


def conc(concs):
    out = []
    for L, occ, R in concs:
        left = escape(' '.join(L))
        right = escape(' '.join(R))
        line = left + '\t' + occ + '\t' + right
        out.append(line)

    return '\n'.join(out)
