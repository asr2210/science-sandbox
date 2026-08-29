"""Experiment 013: 16 buckets, each with a different 4-mer motif at pos 90.

16 buckets of 3125 strings each. Each bucket's motif is a different 4-mer
repeated 5 times (20 chars) inserted at pos 90-109. Background random.

4-mers chosen for diversity:
- 4 monomer-repeats (poly-X)
- 6 distinct pairs (00XX where XX>0)
- 6 permutations of (0,1,2,3)

Tests whether (a) more buckets, (b) more motif diversity boosts signal.
"""
import os
import numpy as np

STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
N_BUCKET = 3125  # 50000 / 16

MOTIFS_4 = [
    "0000", "1111", "2222", "3333",         # monomers
    "0011", "0022", "0033", "1122", "1133", "2233",  # ordered pairs
    "0123", "0132", "0213", "0231", "0312", "0321",  # permutations
]
assert len(MOTIFS_4) == 16

rng = np.random.default_rng(seed=29)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for motif4 in MOTIFS_4:
        motif20 = (motif4 * 5)[:MOTIF_LEN]
        motif_bytes = bytes(motif20, "ascii")
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_bytes[k]
            f.write(chars.decode("ascii") + "\n")
print("done")
