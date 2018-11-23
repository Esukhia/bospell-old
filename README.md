# A framework for spell checking Tibetan.


Processing a given string in bospell means having it pass through the pipeline that consists of four pipes:

 - `a_preprocessing`
 - `b_tokenizers`
 - `c_processors`
 - `d_formatters`

## Demo

    spellcheck_folder(in_dir, out_dir,
                  preproc='corpus',
                  tok='sgmt_corpus',
                  matcher='corpus_cor',
                  format='conc',
                  left=10,
                  right=10)



## Preprocessing

 - Input: `string`
 - Output: `string`

## Tokenizers

 - Input: `string`
 - Output: `list` of tokens

Token types:

 - `Token` object for all tokenizers derived from `pybo`
 - `string` for all others

## Processors

 - Input: `list` of tokens (note that processors expect to be fed with the correct types of tokens)
 - Output: a structure of `string`s

Structure types:

 - concordances: `([<string>, <string>, …], <string>, [<string>, <string>, …])`
 - spellcheck: `list` of `string`s
 - (...) 

This is where the real modifications happen.

Two usecases appear at the moment:

 - apply a given pattern in the token list and organize the matches in a given structure (like creating concordances)
 - apply modifications in the tokens themselves (like correcting misspellings) 

## Formatters

 - Input: structure of `string`s
 - Output: `string` to be written as the final output

## Adding new components

