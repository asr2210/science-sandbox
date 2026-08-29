"""Experiment 010: Markov anti-staying chains.

Each consecutive pair MUST differ. char[i] uniform from {0,1,2,3} \ {char[i-1]}.

- Per-position marginal: uniform (by symmetry of transition matrix).
- Dinucleotide structure: never c->c; uniform over (c -> other 3).
- Per-sequence: random length-200 sequences with no adjacent same char.

Tests if dinucleotide anti-correlation matters.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 31

rng = np.random.default_rng(SEED)
mat = np.empty((N, L), dtype=np.uint8)

# Vectorized Markov: pick all transitions
# transitions[i, j] in {0,1,2}: offset from prev (1, 2, 3 mod 4)
mat[:, 0] = rng.integers(0, 4, size=N, dtype=np.uint8)
transitions = rng.integers(1, 4, size=(N, L - 1), dtype=np.uint8)
for p in range(1, L):
    mat[:, p] = (mat[:, p - 1] + transitions[:, p - 1]) % 4

# Verify
sample = mat[0]
adj_eq = (sample[1:] == sample[:-1]).sum()
assert adj_eq == 0, f"Sample has {adj_eq} adjacent equal chars"
print(f"Sample: {sample[:30]}")
print(f"Pos 0 counts: {np.bincount(mat[:, 0], minlength=4)}")
print(f"Pos 100 counts: {np.bincount(mat[:, 100], minlength=4)}")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in mat:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} Markov anti-staying sequences to {out_path}")
