
def is_tagged_sequence(tokens, token, s_tag, e_tag):
    return token and tokens and tokens[-1]\
           and tokens[-1][-1].strip() == e_tag \
           and token[0].strip() == s_tag


def segment_with_tags(string, start_tag, end_tag, sep):
    """segment on sep, except when sep is found within a tag.
    Also keep together sequences of tagged text

    """
    chunks = []
    inside_tags = False
    chunk = ''
    sep_count = 0
    for char in string:
        if char == start_tag:
            inside_tags = True

        if inside_tags and char == sep:
            sep_count += 1

        if sep_count > 3:
            inside_tags = False
            sep_count = 0

        if inside_tags and char == end_tag:
            chunk += char
            if is_tagged_sequence(chunks, chunk, start_tag, end_tag):
                chunks[-1] += chunk
            else:
                chunks.append(chunk)
            chunk = ''
            inside_tags = False

        elif not inside_tags and char == sep:
            if is_tagged_sequence(chunks, chunk, start_tag, end_tag):
                chunks[-1] += chunk
            else:
                chunks.append(chunk)
            chunk = ''
            sep_count = 0

        else:
            chunk += char

    return chunks


def segmt_corpus(string):
    """Tokenizes string on "\n" and spaces

    :param string: to tokenize
    :return: list of tokens
    """
    string = string.replace('\n', ' ')
    string = string.replace('_', '_ ')  # so that spaces in orig string is used
    return segment_with_tags(string, '༺', '༻', ' ')

