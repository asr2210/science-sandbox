"""4-bucket polyX motif at positions 90-109 (len 20), random background.
This was the v08 best-known recipe (mean_r=0.0061 on eval_01).
Testing whether v14 scorer responds to bucket-structured motif patterns."""
import numpy as np

N_BUCKET = 12_500
L = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

motifs = ["0" * MOTIF_LEN, "1" * MOTIF_LEN, "2" * MOTIF_LEN, "3" * MOTIF_LEN]

with open("libraries/004_motif_buckets_pos90/sequences_0.txt", "w") as f:
    for bucket, motif in enumerate(motifs):
        bg = rng.integers(0, 4, size=(N_BUCKET, L), dtype=np.uint8)
        for row in bg:
            chars = bytearray(L)
            for j in range(L):
                chars[j] = ord('0') + int(row[j])
            for k, c in enumerate(motif):
                chars[MOTIF_START + k] = ord(c)
            f.write(chars.decode("ascii") + "\n")
