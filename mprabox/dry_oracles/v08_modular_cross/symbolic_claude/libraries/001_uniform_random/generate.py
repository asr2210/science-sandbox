"""Experiment 001: Pure uniform random baseline.

50,000 strings of length 200, each character i.i.d. uniform over {0,1,2,3}.
"""
import os
import numpy as np

N = 50_000
L = 200
ALPHABET = "0123"
SEED = 1

rng = np.random.default_rng(SEED)
# generate as integers 0-3 then map to chars
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
table = np.array([ord(c) for c in ALPHABET], dtype=np.uint8)
chars = table[arr]  # ASCII bytes
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
