"""Exp 003: position-indexed gradient.

Sequence i has each character drawn iid from {0,1,2,3} with weights that
shift from (1,0,0,0) at i=0 to (0,0,0,1) at i=N-1, linearly through
(0.5,0.5,0,0), (0,0.5,0.5,0), (0,0,0.5,0.5).

The "average character value" of sequence i correlates monotonically with i,
testing whether any eval rewards correlation between sequence feature and
position index.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(123)

# For each sequence i, derive a "center" c_i in [0, 3].
# Then distribute weight around c_i (triangular).
chars = "0123"
lines = []
for i in range(N):
    c = 3.0 * i / (N - 1)  # in [0, 3]
    # weight for char k: max(0, 1 - |k - c|)
    w = np.maximum(0.0, 1.0 - np.abs(np.arange(4) - c))
    w = w / w.sum()
    idx = rng.choice(4, size=L, p=w)
    lines.append("".join(chars[k] for k in idx))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} lines")
