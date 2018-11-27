def is_tagged_sequence(tokens, token, s_tag, e_tag):
    return token and tokens and tokens[-1]\
           and tokens[-1][-1].strip() == e_tag \
           and token[0].strip() == s_tag


def segment_with_tags(string, start_tag, end_tag, sep, in_tag_max=3):
    """segment a string on sep,
    yet keep everything between start and end tags in a single token.
    To avoid kilometric tokens, stop growing the token when sep has been encountered in_tag_max times.

    limitation: in case a token is truncated, it is left as is, without coming back and
    splitting it on the sep char.
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

        if sep_count > in_tag_max:
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
