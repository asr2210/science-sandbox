"""Exp 002: 50k identical sequences ('0123' repeated 50x = length 200).

Tests whether the scorer is per-sequence (averages to a single value) or
correlation-based (would give NaN/0 from constant predictions).
"""
import os

N = 50_000
SEQ = ("0123" * 50)  # length 200
assert len(SEQ) == 200
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

with open(OUT, "w") as f:
    for _ in range(N):
        f.write(SEQ)
        f.write("\n")
print(f"Wrote {N} identical sequences to {OUT}")
