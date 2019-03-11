
def extract_tib_only(csv_dump):
    lines = csv_dump.strip().split('\n')  # cut dump in lines
    lines = [l.split(',')[1] for l in lines]  # only keep the text
    lines = [lines[i] for i in range(0, len(lines), 2)]  # only keep the tibetan

    return ''.join(lines)


def extract_all(csv_dump):
    lines = csv_dump.strip().split('\n')  # cut dump in lines
    lines = [l.split(',')[1] for l in lines]  # only keep the text
    return ''.join(lines)
