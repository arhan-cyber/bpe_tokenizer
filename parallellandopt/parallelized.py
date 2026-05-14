from multiprocessing import Pool
from pretokenization_example import find_chunk_boundaries
from worker import process_chunk, merge_freq_dicts


def main():
    filename = "TinyStoriesV2-GPT4-valid.txt"

    with open(filename, "rb") as f:
        num_processes = 4

        boundaries = find_chunk_boundaries(
            f,
            num_processes,
            b"<|endoftext|>",
        )

    jobs = [
        (filename, start, end)
        for start, end in zip(boundaries[:-1], boundaries[1:])
    ]

    with Pool(num_processes) as pool:
        partial_freqs = pool.map(process_chunk, jobs)

    freq = merge_freq_dicts(partial_freqs)

    print(freq)


if __name__ == "__main__":
    main()