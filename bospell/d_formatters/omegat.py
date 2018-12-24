from typing import List
import re


def separate_with_dash(tokens: List[str], sep: chr = ' ') -> str:
    tokens = [re.sub(r'་([^ །])', r'-\1', t) for t in tokens]
    return sep.join(tokens)
