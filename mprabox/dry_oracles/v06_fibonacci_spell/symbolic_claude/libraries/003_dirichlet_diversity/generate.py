"""Experiment 003: High-variance compositional library.

For each of 50K sequences, draw a Dirichlet(0.3, 0.3, 0.3, 0.3) prior
to get an extreme per-sequence composition over {0,1,2,3}. Then sample
200 positions from that composition. This creates sequences whose
nucleotide composition varies WIDELY across the library — from nearly
constant ('aaaa...') to balanced.

If the eval model's predictions are sensitive to composition, this should
produce wide variance in predicted activities, raising the Pearson r.
"""
import os
import numpy as np

N_SEQS = 50_000
LEN = 200
ALPHA = 0.3
SEED = 7
ALPHABET = "0123"

rng = np.random.default_rng(SEED)
compositions = rng.dirichlet([ALPHA] * 4, size=N_SEQS)

uniforms = rng.random((N_SEQS, LEN))
cum = np.cumsum(compositions, axis=1)
indices = np.searchsorted_v = np.zeros((N_SEQS, LEN), dtype=np.uint8)
for j in range(LEN):
    indices[:, j] = (uniforms[:, j:j+1] > cum[:, :3]).sum(axis=1)

chars = np.array(list(ALPHABET))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in indices:
        f.write("".join(chars[row]) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
