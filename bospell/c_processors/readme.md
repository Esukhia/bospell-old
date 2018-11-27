# Processing

The list of tokens are processed and transformed.


## Expected In/Out

 - Input: `List[Token]`
 - Output: `Structure`

In the currently implemented functions, `Structure` is either aimed at producing concordances, lists of token types and their frequencies or a string where tokens are separated by spaces

## Content

### Concordances

| component signature                                                                                      |  action                                                |
|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| `def pybo_error_concs(tokens: List[PyboToken], left=5, right=5) -> DefaultDict[str, List[str]]:`         | create concordances of non-words detected by pybo (potential sanskrit is not considered as errors) |
| `def corpus_review_concs(tokens: List[str], left=5, right=5) -> List[Tuple[List[str], str, List[str]]]`  | create concordances of all tokens that require reviewing, <br>either they have the `[` and `]` tags <br>or they have the same content of a token to review without the tags |
| `def corpus_correct_concs(tokens: List[str], left=5, right=5) -> List[Tuple[List[str], str, List[str]]]` | create concordances of all tokens containing either `[` or `]` in them |


### Token types

| component signature                                                       |  action                                                |
|---------------------------------------------------------------------------|--------------------------------------------------------|
| `def pybo_error_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:` | counts all the non-words found by pybo and presents them in reverse frequency order |
| `def pybo_raw_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:`   | counts all tokens found by pybo and presents them in reverse frequency order |


### Separated words


| component signature                                                       |  action                                                |
|---------------------------------------------------------------------------|--------------------------------------------------------|
| `def pybo_raw_content(tokens: List[PyboToken]) -> List[str]:`             | extracts `content` from `PyboToken`s                   |
| `def spaces_plain_fulltext(tokens: List[str]) -> List[str]:`              | placeholder tokenizer                                  |


### Tagged words

TODO