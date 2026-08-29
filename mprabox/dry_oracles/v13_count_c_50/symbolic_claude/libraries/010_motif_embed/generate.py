"""Exp 010: Dirichlet(2.0) backgrounds with embedded per-sequence motifs.

Goal: keep our best composition variance, ADD k-mer variance via embedded
short motifs.

For each sequence:
- Composition ~ Dirichlet(2.0)
- Background sampled from composition
- One random motif of length L_motif ~ U[6, 10]
- Embedded N_copies ~ U[2, 6] times at random non-overlapping positions
"""
import os
import random
import numpy as np

np.random.seed(20260609)
random.seed(20260609)

N = 50_000
L = 200
ALPHA = "0123"
K = 4

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        comp = np.random.dirichlet(np.full(K, 2.0))
        bg_idx = np.random.choice(K, size=L, p=comp)
        bg = [ALPHA[c] for c in bg_idx]

        motif_len = random.randint(6, 10)
        # Choose motif from the same composition (so motif fits sequence style),
        # or independently — try independent for max variety.
        motif = [random.choice(ALPHA) for _ in range(motif_len)]
        n_copies = random.randint(2, 6)
        positions = random.sample(range(L - motif_len + 1), k=n_copies)
        for pos in positions:
            for j in range(motif_len):
                bg[pos + j] = motif[j]

        f.write("".join(bg) + "\n")
print(f"wrote {N} sequences with embedded motifs")
