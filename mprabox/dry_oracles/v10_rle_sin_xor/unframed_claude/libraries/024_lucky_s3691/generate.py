"""per-col balanced uniform 50% GC, seed=3691."""
import os
import numpy as np
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
rng = np.random.default_rng(3691)
base_vec = np.repeat(np.arange(4, dtype=np.int8), N // 4)
m = np.empty((N, L), dtype=np.int8)
for j in range(L):
    m[:, j] = base_vec[rng.permutation(N)]
seqs = ["".join(ALPHABET[r]) for r in m]
open(OUT, "w").write("\n".join(seqs) + "\n")
