"""Binary motif presence: 25k random uniform, 25k same w/ '01230123' inserted at center.

Tests if the model is sensitive to a periodic 8-mer motif. Creates strong variance
in 'has-motif' feature across the 50k.

If model responds: motif-bearing have higher (or lower) M. If target T responds similarly,
correlation grows.
"""
import numpy as np
import os

SEED = 31
N_HALF = 25000
L = 200
MOTIF = "01230123"
ML = len(MOTIF)
INSERT_POS = (L - ML) // 2  # center insertion
ALPHA = "0123"

rng = np.random.default_rng(SEED)

# Random uniform for all 50k
arr = rng.integers(0, 4, size=(2 * N_HALF, L), dtype=np.uint8)
motif_arr = np.array([int(c) for c in MOTIF], dtype=np.uint8)
# Insert motif at center for the first 25k (we'll shuffle order doesn't matter)
arr[:N_HALF, INSERT_POS : INSERT_POS + ML] = motif_arr

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {2*N_HALF} sequences (25k motif + 25k random) to {out_path}")
