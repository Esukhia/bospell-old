from typing import List, Tuple


def basic_conc(concs: List[Tuple[List[str], str, List[str]]], sep: str = '', context_sep: str = ' ', esc_context: bool = True) -> str:
    out = []
    for L, occ, R in concs:
        left = context_sep.join(L)
        right = context_sep.join(R)

        if esc_context:
            left, right = f'"{left}"', f'"{right}"'

        line = f'{left}{sep}{occ}{sep}{right}'
        out.append(line)

    return '\n'.join(out)
