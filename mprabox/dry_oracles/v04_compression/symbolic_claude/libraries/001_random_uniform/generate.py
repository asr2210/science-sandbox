"""Random uniform baseline: 50,000 strings of length 200 over {0,1,2,3}."""
import os
import random

random.seed(42)
N = 50000
L = 200

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = "".join(random.choice("0123") for _ in range(L))
        f.write(s + "\n")

print(f"wrote {N} sequences of length {L} to {out_path}")
