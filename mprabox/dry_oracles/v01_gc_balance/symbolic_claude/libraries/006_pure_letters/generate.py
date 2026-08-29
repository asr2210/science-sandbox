"""
Experiment 006: Pure 4-letter anchor library — only 4 distinct sequences.

Library: 12500 copies each of '0'*200, '1'*200, '2'*200, '3'*200.

With only 4 distinct (f,g) points (replicate weight cancels out of the
Pearson r), this directly measures how well-aligned the 4 letter anchors
are in (f,g) space for each eval.

Possible outcomes:
- If r ≈ 0.7+: letter anchors are strongly aligned and account for most of
  exp 005's gain. Future work should pile on more anchors.
- If r ≈ 0.4-0.5: anchors are moderately aligned.
- If r ≈ 0 or negative: anchors are antagonistic, the gain in 005 came
  from interactions with random strata.
- NaN: f or g is constant across the 4 letters (only one varies).
"""
import os

L = 200
N = 50000
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []
for ch in "0123":
    lines += [ch * L] * 12500

assert len(lines) == N

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {N} sequences (4 distinct templates)")
