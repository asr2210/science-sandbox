"""Experiment 009: Each sequence is a permutation of EXACTLY 50 each of A/C/G/T.

Removes the natural Binomial(200, 0.5) GC variance — every sequence has exactly
50% GC, exactly 25% of each base. Tests whether removing per-sequence
composition noise helps or hurts.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")

rng = np.random.default_rng(20260609)
template = np.array([0] * 50 + [1] * 50 + [2] * 50 + [3] * 50, dtype=np.int8)
assert len(template) == LEN

seqs = []
for _ in range(N_SEQ):
    perm = rng.permutation(template)
    seqs.append("".join(ALPHABET[b] for b in perm))

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} permutation sequences (exact 25%/25%/25%/25%) to {out_path}")
