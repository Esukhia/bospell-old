# Spell-checking utility for Tibetan

## Usage

    from bospell import SpellCheck

    profile = 'pybo_raw_content'
    sc = SpellCheck(profile)

    text = '༄༅།།ཆོས་ཀྱི་སྐུ་ལ་གནས་པའི་ཡོན་ཏན་ཐུན་མོང་མ་ཡིན་པ་ལ་བསྟོད་པ། ༄༅༅།།ཆོས་ཀྱི་སྐུ་ལ་གནས་པའི་ཡོན་ཏན་ཐུན་མོང་མ་ཡིན་པ་ལ་བསྟོད་པ། དེ་བཞིན་གཤེགས་པ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །'
    out = sc.check(text)

    print(out)
    >>> ༄༅།། ཆོས་ ཀྱི་ སྐུ་ ལ་ གནས་པ འི་ ཡོན་ཏན་ ཐུན་མོང་ མ་ཡིན་པ་ ལ་ བསྟོད་པ ། ༄༅༅།། ཆོས་ ཀྱི་ སྐུ་ ལ་ གནས་པ འི་ ཡོན་ཏན་ ཐུན་མོང་ མ་ཡིན་པ་ ལ་ བསྟོད་པ ། དེ་བཞིན་གཤེགས་པ་ ཐམས་ཅད་ ལ་ ཕྱག་ འཚལ་ ལོ ། ། 

## Build your own pipeline

Check for `bospell.yaml` in the folder where `check()` was called for examples.

Read the four pipe's readmes for all the available components and what they do [preprocessing](./bospell/a_preprocessing/readme.md), [tokenizing](./bospell/b_tokenizers/readme.md), [processing](./bospell/c_processors/readme.md), [formatting](./bospell/d_formatters/readme.md).


## Contributing

How to contribute is explained [here](./bospell/readme.md).


## License

The Python code is Copyright (C) 2018 Esukhia, provided under [MIT License](LICENSE).