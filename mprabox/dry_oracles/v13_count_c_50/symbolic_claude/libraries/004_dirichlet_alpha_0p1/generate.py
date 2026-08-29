"""Exp 004: more extreme Dirichlet(0.1) compositions.

Compositions are pushed closer to the simplex corners. With alpha=0.1, many
sequences are near-constant in one character (so we expect higher variance
in any composition-based prediction).

Safeguard: clip composition floor to avoid producing exactly identical
all-same-character sequences (which caused NaN in exp 002).
"""
import os
import numpy as np

np.random.seed(20260603)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]

alpha = np.full(4, 0.1)
comps = np.random.dirichlet(alpha, size=N)

# Floor: ensure every composition has at least 1% in every character so
# sampled sequences have some chance of non-degenerate content.
comps = np.clip(comps, 0.005, None)
comps = comps / comps.sum(axis=1, keepdims=True)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        p = comps[i]
        seq_chars = np.random.choice(ALPHA, size=L, p=p)
        f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences with Dirichlet(0.1) compositions (floor 0.005)")
