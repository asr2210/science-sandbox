"""Experiment 004: Two halves with disjoint alphabets.

First 25 000 strings: random uniform over {0, 1}.
Second 25 000 strings: random uniform over {2, 3}.

If the scorer's per-string feature distinguishes between these two
populations (e.g. is something like GC content under a 0=A,1=C,2=G,3=T
mapping, or DNA-like motifs), then condition_a should be a non-zero
correlation (sign tells us which half the target prefers).
"""
import os
import numpy as np

N_HALF = 25_000
STR_LEN = 200
rng = np.random.default_rng(seed=11)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    # First half: only {0, 1}
    a = rng.integers(0, 2, size=(N_HALF, STR_LEN), dtype=np.uint8)
    for row in a:
        f.write("".join(chr(c + ord('0')) for c in row) + "\n")
    # Second half: only {2, 3}
    b = rng.integers(2, 4, size=(N_HALF, STR_LEN), dtype=np.uint8)
    for row in b:
        f.write("".join(chr(c + ord('0')) for c in row) + "\n")

print("done")
