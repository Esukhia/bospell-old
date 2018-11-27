# Formatters

The output of processors is formatted so it can be written in output files


## Expected In/Out

 - Input: `Structure`
 - Output: `str`

see tokenizers for `Structure`


## Content

### Concordances

| component signature                                                                                                                      |  action                                                |
|------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| `def basic_conc(concs: List[Tuple[List[str], str, List[str]]], sep: chr = '', context_sep: chr = ' ', esc_context: bool = True) -> str:` | format for rows: `<left><sep><occurence><sep><right>`<br>default values: <ul><li>token separator in contexts: ` `</li><li>column separator: `\t`</li></ul> |


### Token types

| component signature                                                               |  action                                                |
|-----------------------------------------------------------------------------------|--------------------------------------------------------|
| `def stats_types(total_mistakes: DefaultDict[str, int], sep: chr = '\t') -> str:` | format for rows: `<type><sep><count>`<br>default column separator: `\t` |


### Separated words

| component signature                                                       |  action                                                |
|---------------------------------------------------------------------------|--------------------------------------------------------|
| `def plaintext(tokens: List[str], sep: chr = ' ') -> str:`                | separates tokens with `sep` (default: space)           |


### Tagged words

TODO