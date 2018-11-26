from pybo import BoTokenizer, Token
from typing import NewType, List

PyboToken = NewType('PyboToken', Token)


def pybo_tok(text: str, profile: str) -> List[PyboToken]:
    tok = BoTokenizer(profile)
    return tok.tokenize(text)
