import pretokenization_example
from pretokenization_example import find_chunk_boundaries
from multiprocessing import Pool
from collections import defaultdict





#=======this is the single threaded code======
def build_local_freq(pretokens):
    freq = {}

    for token in pretokens:
        token_bytes = token.encode("utf-8")

        byte_tuple = tuple(bytes([b]) for b in token_bytes)

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


#=====one the single threaded code gets byte pair frequency per chunk, we'll merge globally
def merge_freq_dicts(dicts):
    merged = defaultdict(int)

    for d in dicts:
        for token, count in d.items():
            merged[token] += count

    return dict(merged)


if __name__ == "__main__":

    filename = "TinyStoriesV2-GPT4-valid.txt"

    with open(filename, "rb") as f:
        num_processes = 4

        boundaries = find_chunk_boundaries(
            f,
            num_processes,
            b"<|endoftext|>",
        )

    # one thread per chunk
    jobs = [
        (filename, start, end)
        for start, end in zip(boundaries[:-1], boundaries[1:])
    ]

    # Parallel processing
    with Pool(num_processes) as pool:
        partial_freqs = pool.map(process_chunk, jobs)

    # Merge all chunkwise
    freq = merge_freq_dicts(partial_freqs)

    print("global freq dictionary:")
    print(freq)