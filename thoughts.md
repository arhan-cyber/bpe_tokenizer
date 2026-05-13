At the current state, the byte_bpe function takes in the pretokenized text and num_iters as parameters.
However, a pitfall it has currently is that it writes directly to vocabulary, this is undesirable ( I think so as of now).
If we were to just return the byte pair merges , then it could be easier to parallelize as we obtain the merges from each of the individual threads and then append them all to the vocabulary at once.

On the other hand, if we were to pass the vocabulary as an argument to the byte_bpe function, and if it were to be parallelized and all of the individual threads could write directly to the vocabulary, we wouldn't have to wait for all of them to finish before appending all at once. I do not know however if this might create read/write lock issues or smth.


After some research, I believe that adding locks to the parallelized is a bad idea as it might cause too much wait time, we'll just have the byte_bpe function return the merges.