"""Experiment 016: Uniform random seed=77777."""
import os, numpy as np
N, L, SEED = 50000, 200, 77777
rng = np.random.default_rng(SEED)
chars = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in chars:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} uniform random seed=77777")
