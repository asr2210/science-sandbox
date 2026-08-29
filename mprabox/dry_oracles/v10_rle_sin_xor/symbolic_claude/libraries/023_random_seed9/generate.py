#!/usr/bin/env python3
import random, os
random.seed(9)
N, L = 50000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choice("0123") for _ in range(L)) + "\n")
print(f"Wrote {N} sequences seed=9")
