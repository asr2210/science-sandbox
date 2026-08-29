"""Index encoding: seq i's first 9 positions are base-4 digits of i.
Rest random uniform. Probes whether scorer extracts per-seq index information."""
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
PREFIX = 9  # 4^9 = 262144 > 50000

with open("libraries/011_index_encoded/sequences_0.txt", "w") as f:
    for i in range(N):
        digits = []
        x = i
        for _ in range(PREFIX):
            digits.append(x % 4)
            x //= 4
        digits.reverse()
        tail = rng.integers(0, 4, size=L - PREFIX, dtype=np.int8).tolist()
        seq_chars = "".join(map(str, digits)) + "".join(map(str, tail))
        f.write(seq_chars + "\n")
