# Tokenizing

The input string is turned into a list of tokens.

## Expected In/Out

 - Input: `string`
 - Output: `List[Token]`
 
In the currently implemented functions, a `Token` is either a `str` or a `PyboToken`.

## Content

| component signature                                         |  action                                                |
|-------------------------------------------------------------|--------------------------------------------------------|
| `def space_tok(text: str) -> List[str]:`                    | splits a `str` strictly on spaces.                     |
| `def corpus_tok_to_correct(text: str) -> List[str]:`        | Tokenizes on spaces and \n, while keeping together the content of `[` and `]` tags |
| `def corpus_tok_vernacular(text: str) -> List[str]:`        | Tokenizes on spaces and \n, while keeping together the content of `༺` and `༻` tags  |
| `def pybo_tok(text: str, profile: str) -> List[PyboToken]:` | Produces pybo tokens |