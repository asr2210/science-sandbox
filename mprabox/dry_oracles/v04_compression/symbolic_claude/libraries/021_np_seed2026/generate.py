"""numpy PCG64 seed=2026."""
import os, numpy as np
rng = np.random.default_rng(2026)
arr = rng.integers(0, 4, size=(50000, 200), dtype=np.int8)
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    for row in arr:
        f.write("".join(map(str, row.tolist())) + "\n")
print("done seed=2026")
