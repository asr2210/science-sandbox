"""Experiment 002: Single random string repeated 50,000 times.

Zero library diversity, uniform per-string composition. If score
drops vs 001, diversity matters; if equal, only per-string
composition or single-string properties matter.
"""
import os
import random

random.seed(1)

N = 50_000
L = 200
ALPHABET = "0123"

s = "".join(random.choice(ALPHABET) for _ in range(L))

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(s + "\n")

print(f"Wrote {N} copies of one string to {out_path}")
print(f"String head: {s[:40]}")
