# Components

See the corresponding readmes: [preprocessing](./a_preprocessing/readme.md), [tokenizing](./b_tokenizers/readme.md), [processing](./c_processors/readme.md), [formatting](./d_formatters/readme.md)

All the components for each of these four pipes are gathered in the respective `__init__.py`.
From there, they are centralized in the [general `__init__.py`](./__init__.py#L3-L7).


Each component is finally brought in the corresponding section of [components](./__init__.py#L14-L44), where it is linked to a key (a `str`) so it can be used by the `SpellCheck` class.


# SpellCheck class

## Profiles

Pipeline profiles and related arguments are passed in by the [Config](./config.py) class.
The list of default profiles are found [here](./config.py#L5)

## Validity check

 - The values of a pipeline corresponding to a profile [is checked](./__init__.py#L113-L121) against `components` to make sure the profile is valid.
 - The pipes are then [checked](./__init__.py#L123-L142):
    - a pipeline must contain at least: a tokenizer, a processor and a formatter
    - pipes must be compatible with each other:
        - pybo tokenizers must be followed by pybo processors
        - token types processors must be followed by types formatters
        - concordance processors must be followed by concordance formatters

## Running the pipeline

The [check()](./__init__.py#L69) method fetches the corresponding functions in `components` and runs the pipeline.


# CheckFile class

It is a facility class to process a file at a time.


# Adding components

1. Add a function in the corresponding pipe-folder (if there is a `helpers.py` file, there might be something useful for new components)
2. Ensure to import the new function in both the pipe's and the general `__init__.py`.
3. Add the new component in [components](./__init__.py#L14-L44), choosing a unique key for it.
4. If the component has compatibility requirements, make sure to add tests in [is_valid_pipeline()](./__init__.py#L123-L142)
5. Consider adding a default profile [here](./config.py#L5) for ease of use, both for yourself and others.
