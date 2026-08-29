"""Exp 004: balanced composition + random ordering.

Each sequence: exactly 50 of each base (0,1,2,3), permuted uniformly
at random. This freezes composition (perfectly balanced) and varies
only the ordering. Compared to Exp 001 (uniform random ~ binomially
balanced), this should tell us whether the small composition variance
of pure random matters.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200  # 50 * 4
SEED = 4

base_template = np.repeat(np.arange(4, dtype=np.uint8), L // 4)  # 50 each
rng = np.random.default_rng(SEED)

# Independently permute each sequence
# argsort of random keys gives permutation indices
keys = rng.random((N, L))
perm_idx = keys.argsort(axis=1)
seqs = base_template[perm_idx]  # (N, L)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

# sanity: per-row counts
counts = (seqs[:, :, None] == np.arange(4)[None, None, :]).sum(axis=1)
print(f"wrote {N} sequences; counts per base (min,max) = {counts.min(axis=0)}, {counts.max(axis=0)}")
