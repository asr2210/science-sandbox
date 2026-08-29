"""Exp 001: baseline of 50k uniform random strings, length 200, alphabet {0,1,2,3}."""
import os
import numpy as np

N = 50_000
L = 200
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(0)
arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
# Convert each row to ascii string '0'-'3'
arr += ord('0')
with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(arr[i].tolist()))
        f.write(b"\n")
print(f"Wrote {N} sequences to {OUT}")
