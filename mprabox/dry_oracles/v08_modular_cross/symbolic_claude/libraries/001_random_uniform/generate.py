import numpy as np
import os

SEED = 42
N = 50000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
