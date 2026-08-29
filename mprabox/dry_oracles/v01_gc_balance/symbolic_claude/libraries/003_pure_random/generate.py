"""
Experiment 003: 100% uniform random library.

Pure baseline. Predicts: should beat exp 001's 0.5436 because we've
removed the variance-killing constant/periodic strata.
"""
import os, random

random.seed(3)

L = 200
N = 50000
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = ["".join(random.choices(ALPHABET, k=L)) for _ in range(N)]

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {N} uniform random sequences to {OUT}")
