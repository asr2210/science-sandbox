"""Experiment 009: Perfect per-column nucleotide balance.

For each of 200 columns, the column contains exactly 12500 A, 12500 C,
12500 G, 12500 T in a random row order. Each row of the matrix is one
sequence (across columns). Random uniform i.i.d. has per-column binomial
sampling noise (~±100 around 12500); this removes that noise.

If T5 is right (any reduction in library-wide variance hurts), this might
DROP the score. If perfect column balance removes "useless noise" that the
scorer doesn't care about, this might be flat or slightly positive.
Either result is informative.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 49

assert N_SEQ % 4 == 0
PER_BASE = N_SEQ // 4

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

mat = np.empty((N_SEQ, LEN), dtype=np.int8)
template = np.repeat(np.arange(4, dtype=np.int8), PER_BASE)  # [0]*12500 + [1]*12500 + ...
for j in range(LEN):
    col = template.copy()
    rng.shuffle(col)
    mat[:, j] = col

seqs = ["".join(row) for row in bases[mat]]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs; each column has exactly {PER_BASE} of each base")
