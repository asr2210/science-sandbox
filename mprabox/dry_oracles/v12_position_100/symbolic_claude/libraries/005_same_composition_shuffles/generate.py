"""Exp 005: 50K sequences, each a permutation of a fixed composition.

Each sequence has exactly 50 each of 0,1,2,3. Different ORDERINGS only.

Tests: does ORDER matter? If only composition matters, this gives near-zero
(no across-position variance in composition features). If positional/motif
features matter, this gives non-zero.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(7)
base = np.array([0]*50 + [1]*50 + [2]*50 + [3]*50, dtype=np.uint8)
assert base.size == L
chars = np.array(list("0123"))

lines = []
for i in range(N):
    perm = rng.permutation(base)
    lines.append("".join(chars[perm]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} same-composition shuffles")
