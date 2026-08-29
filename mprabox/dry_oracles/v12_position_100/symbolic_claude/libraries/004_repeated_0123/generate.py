"""Exp 004: 50K copies of one non-constant sequence ("0123" repeated to length 200).

If score is per-sequence pearson(seq, target_eval): well-defined per eval.
If score is per-library (requires across-sequence variance): NaN.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
PAT = "0123"
seq = (PAT * ((L // len(PAT)) + 1))[:L]
assert len(seq) == L

with open(OUT, "w") as f:
    for _ in range(N):
        f.write(seq + "\n")
print(f"wrote {N} copies of {seq[:20]}...")
