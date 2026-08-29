"""Experiment 006: Dirichlet(0.05) extreme compositions.

Push compositional variance to the extreme: alpha=0.05 produces almost
vertex-only distributions (each sequence dominated by ~1 nucleotide).
Compare to Dirichlet(0.3)=0.135 from exp 003 to see if pure composition
saturates or continues to climb.
"""
import os
import numpy as np

N_SEQS = 50_000
LEN = 200
ALPHA = 0.05
SEED = 31
ALPHABET = "0123"

rng = np.random.default_rng(SEED)
compositions = rng.dirichlet([ALPHA] * 4, size=N_SEQS)
cum = np.cumsum(compositions, axis=1)
uniforms = rng.random((N_SEQS, LEN))
indices = np.zeros((N_SEQS, LEN), dtype=np.uint8)
for j in range(LEN):
    indices[:, j] = (uniforms[:, j:j+1] > cum[:, :3]).sum(axis=1)

chars = np.array(list(ALPHABET))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in indices:
        f.write("".join(chars[row]) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
