"""Experiment 001: Uniform random baseline.

Generate 50,000 strings of length 200 over {0,1,2,3} uniformly at random.
This establishes a baseline against which other strategies are compared.
"""
import os
import random

N = 50_000
L = 200
ALPHA = "0123"

random.seed(42)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = "".join(random.choice(ALPHA) for _ in range(L))
        f.write(s + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
