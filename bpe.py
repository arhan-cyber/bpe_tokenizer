from collections import defaultdict
vocabulary = {bytes([i]): i for i in range(256)}
vocabulary["<|endoftext|>"]=len(vocabulary)+1
corpus = """low low low low low
lower lower widest widest widest
newest newest newest newest newest newest"""
pretokens = corpus.split()
def byte_bpe(pretokens, num_iterations=5):
    freq = {}
    for token in pretokens:
        token_bytes = token.encode("utf-8")
        byte_tuple = tuple(bytes([b]) for b in token_bytes)
        freq[byte_tuple] = freq.get(byte_tuple, 0) + 1

    print("init freq dictionary:")
    print(freq)

    # bpe merger
    for iteration in range(num_iterations):
        pair_freq = defaultdict(int)
        for byte_tuple, count in freq.items():
            for i in range(len(byte_tuple) - 1):
                byte_pair = (byte_tuple[i], byte_tuple[i+1])
                pair_freq[byte_pair] += count

        if not pair_freq:
            print(f"No more pairs to merge at iteration {iteration}.")
            break

        # lexicographic max freq
        max_freq = max(pair_freq.values())
        candidates = [pair for pair, freq_val in pair_freq.items() if freq_val == max_freq]
        max_pair = max(candidates)

        print(f"Iteration {iteration+1}: Chosen pair to merge:", max_pair)

        # Merge the chosen pair in all tokens
        new_freq = {}
        for byte_tuple, count in freq.items():
            i = 0
            new_tuple = []
            while i < len(byte_tuple):
                if i < len(byte_tuple) - 1 and (byte_tuple[i], byte_tuple[i+1]) == max_pair:
                    merged_byte = byte_tuple[i] + byte_tuple[i+1]
                    new_tuple.append(merged_byte)
                    #added rule for adding merged_byte to vocabulary
                    if merged_byte not in vocabulary:
                        vocabulary[merged_byte] = len(vocabulary)
                    i += 2
                else:
                    new_tuple.append(byte_tuple[i])
                    i += 1
            new_freq[tuple(new_tuple)] = count
        freq = new_freq

        print(f"Updated freq dictionary after iteration {iteration+1}:")
        print(freq)

    return freq

final_freq = byte_bpe(pretokens, num_iterations=6)
print (vocabulary)