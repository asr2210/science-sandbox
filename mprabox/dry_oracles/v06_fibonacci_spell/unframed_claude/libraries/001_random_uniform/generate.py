"""Experiment 001: uniform random baseline.

Generate 50,000 200bp sequences with uniform A/C/G/T at each position.
Purpose: establish a baseline for what 'no biology' looks like across the
14 eval sets.
"""
import os
import numpy as np

N_SEQ = 50_000
LENGTH = 200
ALPHA = np.array(list("ACGT"))

rng = np.random.default_rng(0)

# Sample positions: shape (N_SEQ, LENGTH) of indices 0..3
idx = rng.integers(0, 4, size=(N_SEQ, LENGTH), dtype=np.uint8)
chars = ALPHA[idx]  # (N_SEQ, LENGTH) of single-character strings

# Join each row
lines = ["".join(row) for row in chars]
assert len(lines) == N_SEQ
assert all(len(s) == LENGTH for s in lines)
assert all(set(s) <= set("ACGT") for s in lines[:1000])  # spot check

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines))
    f.write("\n")

print(f"Wrote {N_SEQ} sequences of length {LENGTH} to {out_path}")
