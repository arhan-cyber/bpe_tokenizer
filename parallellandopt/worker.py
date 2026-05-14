from collections import defaultdict


def build_local_freq(pretokens):
    freq = {}

    for token in pretokens:
        token_bytes = token.encode("utf-8")
        byte_tuple = tuple(token_bytes)

        freq[byte_tuple] = freq.get(byte_tuple, 0) + 1

    return freq


def process_chunk(args):
    filename, start, end = args

    with open(filename, "rb") as f:
        f.seek(start)

        chunk = f.read(end - start).decode(
            "utf-8",
            errors="ignore",
        )

    pretokens = chunk.split()

    return build_local_freq(pretokens)


def merge_freq_dicts(dicts):
    merged = defaultdict(int)

    for d in dicts:
        for token, count in d.items():
            merged[token] += count

    return dict(merged)