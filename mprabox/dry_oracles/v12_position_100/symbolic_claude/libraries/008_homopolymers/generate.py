"""Exp 008: 50K homopolymers split equally across 4 chars.

12.5K seqs of '0'*200, 12.5K of '1'*200, etc. Maximum compositional extremity
(corner of simplex), but only 4 distinct values across the library.
Tests upper limit of composition-only signal.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

per = N // 4
lines = []
for c in "0123":
    lines.extend([c * L] * per)

# Shuffle so positions are interleaved (avoid block ordering effects)
rng = np.random.default_rng(17)
rng.shuffle(lines)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} shuffled homopolymers")
