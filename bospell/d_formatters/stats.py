from typing import DefaultDict


def stats_types(total_mistakes: DefaultDict[str, int], sep: chr = '\t') -> str:
    total = [(mis, freq) for mis, freq in total_mistakes.items()]
    total = sorted(total, reverse=True, key=lambda x: x[1])
    total = [f'{mis}{sep}{freq}' for mis, freq in total]
    return '\n'.join(total)
