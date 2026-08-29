"""Random uniform baseline: 50,000 strings of length 200 over {0,1,2,3}."""
import numpy as np
import os

N = 50_000
L = 200
rng = np.random.default_rng(seed=42)
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(chr(48 + b) for b in row) + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
