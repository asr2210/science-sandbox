"""Experiment 006: 50k copies of ONE fixed random sequence.

The sequence uses all 4 chars (with high prob given length 200).
But population at each position is constant (all 50k have same char there).

Distinguishes per-sequence vs population-level scoring:
- If finite score: per-sequence scoring
- If NaN: population-level scoring
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 17

rng = np.random.default_rng(SEED)
seq = rng.integers(0, 4, size=L, dtype=np.uint8)
# Verify all 4 chars present
unique = np.unique(seq)
assert len(unique) == 4, f"Need all 4 chars, got {unique}"
seq_str = "".join(map(str, seq.tolist()))
print(f"Fixed sequence (first 50): {seq_str[:50]}")
print(f"Char counts: {np.bincount(seq, minlength=4)}")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(seq_str)
        f.write("\n")
print(f"Wrote {N} copies of fixed random sequence to {out_path}")
