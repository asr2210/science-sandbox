"""Experiment 005: 4 motif buckets with random backgrounds.

Each string: 200 random uniform chars, EXCEPT positions 90-109 contain
a 20-character "motif" specific to the bucket.
- Bucket 1 (i=0..12499):     poly-'0'  (0000...0)
- Bucket 2 (i=12500..24999): poly-'1'  (1111...1)
- Bucket 3 (i=25000..37499): poly-'2'  (2222...2)
- Bucket 4 (i=37500..49999): poly-'3'  (3333...3)

Background per string is unique random → no constant input.
If the scorer's per-string feature responds to motif identity, we
should see condition_a deviate from 0 (with sign showing preference).
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

motifs = ["0" * MOTIF_LEN, "1" * MOTIF_LEN,
          "2" * MOTIF_LEN, "3" * MOTIF_LEN]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket, motif in enumerate(motifs):
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(b"0") * STR_LEN
            for j in range(STR_LEN):
                chars[j] = ord('0') + int(row[j])
            for k, c in enumerate(motif):
                chars[MOTIF_START + k] = ord(c)
            f.write(chars.decode("ascii") + "\n")

print("done")
