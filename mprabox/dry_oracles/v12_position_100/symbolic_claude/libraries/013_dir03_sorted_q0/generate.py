"""Exp 013: Dir(0.3) library, sorted by q0 (descending).

Tests if position ORDER matters. Dir(0.3) random gave 0.0774 on eval_01.
If sorted gives different score, y_i has positional structure aligned with q0.
If same, position order doesn't matter; library is what counts.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(11)  # SAME seed as exp 006 to start with identical compositions
weights = rng.dirichlet([0.3] * 4, size=N)
chars = np.array(list("0123"))

# Compute q0 for each seq composition
q0 = weights[:, 0]
# Sort descending by q0
order = np.argsort(-q0)
weights = weights[order]

lines = []
for i in range(N):
    idx = rng.choice(4, size=L, p=weights[i])
    lines.append("".join(chars[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} sorted-by-q0 seqs")
