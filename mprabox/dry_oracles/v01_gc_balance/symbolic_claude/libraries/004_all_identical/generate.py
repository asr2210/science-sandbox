"""
Experiment 004: 100% all-identical library.

All 50,000 seqs are identical: '0' * 200.
- If metric is correlation between two latent outputs across the bag:
  zero variance in input → constant output → r = NaN/0.
- If metric is per-seq aggregate (e.g., mean predicted activity):
  some non-zero defined value.

Strong fork test for theory v2.
"""
import os

L = 200
N = 50000
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

seq = "0" * L
lines = [seq] * N

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {N} copies of all-0 to {OUT}")
