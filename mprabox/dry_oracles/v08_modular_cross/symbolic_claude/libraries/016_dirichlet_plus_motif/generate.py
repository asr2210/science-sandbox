"""Dirichlet(0.5) base + binary motif variance.

25k Dirichlet(0.5) compositions, drawn iid.
25k Dirichlet(0.5) compositions, drawn iid, with motif '01230123' inserted at center.

Combines:
- Dirichlet composition diversity (good for eval_01 condition_c)
- Random per-position draws (preserves entropy → condition_b)
- Binary motif-presence variance (helps eval_01 condition_c per exp 008)
"""
import numpy as np
import os

SEED = 191
N_HALF = 25000
L = 200
ALPHA = "0123"
MOTIF = "01230123"
ML = len(MOTIF)
INSERT_POS = (L - ML) // 2

rng = np.random.default_rng(SEED)

# Combined: sample 50k Dirichlet compositions then per-seq draws
probs = rng.dirichlet(np.full(4, 0.5), size=2 * N_HALF)
arr = np.empty((2 * N_HALF, L), dtype=np.uint8)
for i in range(2 * N_HALF):
    arr[i] = rng.choice(4, size=L, p=probs[i])

# Insert motif in first half
motif_arr = np.array([int(c) for c in MOTIF], dtype=np.uint8)
arr[:N_HALF, INSERT_POS : INSERT_POS + ML] = motif_arr

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {2*N_HALF} (Dirichlet 0.5 + half-motif) sequences to {out_path}")
