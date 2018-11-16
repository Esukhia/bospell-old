
def conc(concs):
    out = []
    for L, occ, R in concs:

        line = ''.join(L) + '|— ' + occ + ' —|' + ''.join(R)
        out.append(line)

    return '\n'.join(out)
