"""Experiment 017: 4 buckets with dimer-alternating motifs at pos 90.

Tests whether dinucleotide-pattern motifs differ from poly-X.
- Bucket 1: "01010101010101010101"
- Bucket 2: "12121212121212121212"
- Bucket 3: "23232323232323232323"
- Bucket 4: "30303030303030303030"

Same layout as exp 005 (4 buckets ×12500, motif length 20 at pos 90,
random bg per string). If higher than exp 5 (0.0061) for eval_01,
dimer content matters.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

motifs = [
    "01010101010101010101",
    "12121212121212121212",
    "23232323232323232323",
    "30303030303030303030",
]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for motif in motifs:
        motif_bytes = motif.encode("ascii")
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_bytes[k]
            f.write(chars.decode("ascii") + "\n")
print("done")
