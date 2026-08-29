"""Generate 50,000 uniform random strings of length 200 over {0,1,2,3}."""
import numpy as np
import os

rng = np.random.default_rng(42)
N, L = 50000, 200
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
