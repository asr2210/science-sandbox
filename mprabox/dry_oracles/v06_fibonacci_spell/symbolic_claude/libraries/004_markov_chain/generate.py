"""Experiment 004: Per-sequence random Markov chain.

Each of 50K sequences uses its OWN 4x4 transition matrix where each row
is drawn from Dirichlet(0.3). This adds dinucleotide structure variance
on top of compositional variance. If the eval model is sensitive to
dinucleotide patterns (which CNN-style DNA models typically are), this
should push prediction variance — and thus Pearson r — higher than
the pure Dirichlet-composition experiment 003.
"""
import os
import numpy as np

N_SEQS = 50_000
LEN = 200
ALPHA = 0.3
SEED = 11
ALPHABET = "0123"

rng = np.random.default_rng(SEED)

# Build per-sequence transition matrices and initial distributions
# Vectorize: for each of N_SEQS, draw 4 Dirichlet rows + 1 init
init = rng.dirichlet([ALPHA] * 4, size=N_SEQS)  # (N, 4)
trans = rng.dirichlet([ALPHA] * 4, size=(N_SEQS, 4))  # (N, 4, 4)

# Precompute cumulative for sampling
init_cum = np.cumsum(init, axis=1)  # (N, 4)
trans_cum = np.cumsum(trans, axis=2)  # (N, 4, 4)

# Sample sequences
seqs = np.zeros((N_SEQS, LEN), dtype=np.uint8)
u = rng.random(N_SEQS)
seqs[:, 0] = (u[:, None] > init_cum[:, :3]).sum(axis=1)
for j in range(1, LEN):
    prev = seqs[:, j-1]
    u = rng.random(N_SEQS)
    row_cum = trans_cum[np.arange(N_SEQS), prev, :3]  # (N, 3)
    seqs[:, j] = (u[:, None] > row_cum).sum(axis=1)

chars = np.array(list(ALPHABET))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(chars[row]) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
