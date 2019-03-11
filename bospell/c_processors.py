from collections import defaultdict

from .helpers import is_mistake


def find_mistake_concs(tokens, context=5):
    mistakes = defaultdict(list)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            if num - context < 0:
                left = tokens[:num]
            else:
                left = tokens[num - context:num]
            if num + context > len(tokens)-1:
                right = tokens[num+1:]
            else:
                right = tokens[num+1:num+1+context]

            left = [t.content for t in left]
            right = [t.content for t in right]
            mis = t.content.replace('\n', '\\n')
            mistakes[mis].append([''.join(left), ''.join(right)])

    return mistakes


def find_mistake_types(tokens):
    mistakes = defaultdict(int)
    for token in tokens:
        if is_mistake(token):
            mistakes[token.content] += 1

    return mistakes
