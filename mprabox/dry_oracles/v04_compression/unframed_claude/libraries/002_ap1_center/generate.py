"""Experiment 002: AP-1 motif (TGAGTCA) inserted at center.

Tests whether a single canonical strong activator motif at position 96-102
of an otherwise-random 200bp sequence raises the score.

Variation in the 193bp of flanking sequence preserves Pearson dynamic range,
so this should be a clean test of "does motif presence move the score".
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
MOTIF = "TGAGTCA"
INSERT_POS = (LEN - len(MOTIF)) // 2  # 96
SEED = 43

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
mat = bases[idx]
motif_arr = np.array(list(MOTIF))
mat[:, INSERT_POS:INSERT_POS + len(MOTIF)] = motif_arr

seqs = ["".join(row) for row in mat]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences x {LEN}bp; AP-1 ({MOTIF}) at pos {INSERT_POS}")
