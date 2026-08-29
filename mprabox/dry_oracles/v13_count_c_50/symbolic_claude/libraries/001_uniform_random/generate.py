"""Exp 001: uniform random baseline."""
import os
import random

random.seed(20260602)

N = 50_000
L = 200
ALPHA = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = "".join(random.choices(ALPHA, k=L))
        f.write(s + "\n")
print(f"wrote {N} sequences of length {L} to {out_path}")
