"""AT-biased uniform random.

50k sequences, each char drawn iid from p=(0.4, 0.1, 0.1, 0.4).
All sequences have similar AT-rich composition (no diversity in composition).

If a specific bias direction helps, this will tell us.
"""
import numpy as np
import os

SEED = 149
N = 50000
L = 200
ALPHA = "0123"
P = np.array([0.4, 0.1, 0.1, 0.4])

rng = np.random.default_rng(SEED)
arr = rng.choice(4, size=(N, L), p=P).astype(np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} AT-biased (0.4/0.1/0.1/0.4) sequences to {out_path}")
