from pybo import BoTokenizer, Token, PyBoChunk
from typing import NewType, List

PyboToken = NewType('PyboToken', Token)


def pybo_tok(text: str, profile: str) -> List[PyboToken]:
    tok = BoTokenizer(profile)
    return tok.tokenize(text)


def pybo_syl_tok(text: str) -> List[str]:
    chunks = PyBoChunk(text)
    output = chunks.chunk()
    with_substrings = chunks.get_chunked(output)
    return [b for a, b in with_substrings]
