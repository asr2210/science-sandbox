"""Experiment 005: 1st-order Markov sequences with human-like dinucleotide
frequencies (CpG strongly depressed).

Tests T_real_dna: whether scorers trained on natural human DNA give
HIGHER r on real-looking sequences than uniform random.

Approximate transition matrix P(next | current). Constructed so that:
- Marginal frequencies are A=T~0.295, C=G~0.205 (human-like).
- CpG (G after C) is strongly depressed (0.05 vs naive 0.20).
- Other dinucleotides near naive expectation.

I rebalanced rows to sum to 1 after specifying key entries.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 45

# rows = current base, cols = next base. order = A, C, G, T
T = np.array([
    [0.32, 0.21, 0.27, 0.20],  # from A
    [0.36, 0.27, 0.05, 0.32],  # from C   <- CpG depression
    [0.30, 0.22, 0.27, 0.21],  # from G
    [0.20, 0.21, 0.27, 0.32],  # from T
])
T = T / T.sum(axis=1, keepdims=True)

# Initial distribution
pi = np.array([0.295, 0.205, 0.205, 0.295])
pi = pi / pi.sum()

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# Vectorised generation: for each position, given current base index per seq,
# sample next from T[current_idx]. Loop over LEN positions.
mat = np.empty((N_SEQ, LEN), dtype=np.int8)
mat[:, 0] = rng.choice(4, size=N_SEQ, p=pi)

# Precompute cumulative for each row for fast sampling
cum = np.cumsum(T, axis=1)  # (4, 4)
for j in range(1, LEN):
    u = rng.random(N_SEQ)
    cur = mat[:, j - 1]
    # cum[cur] has shape (N_SEQ, 4); find first col where u < cum
    nxt = (u[:, None] < cum[cur]).argmax(axis=1)
    mat[:, j] = nxt

seqs = ["".join(row) for row in bases[mat]]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs x {LEN}bp; 1st-order Markov, CpG-depleted")
