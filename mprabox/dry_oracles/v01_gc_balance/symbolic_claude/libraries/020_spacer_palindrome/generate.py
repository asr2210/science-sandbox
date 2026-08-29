"""
Experiment 020: Spacer-flanked palindrome.

Each sequence = first_half (90bp) + spacer (20bp random) + RC of
first_half (90bp). Total 200bp.

Models a dimer TF binding site with a central random spacer.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SPACER = 20
HALF = (L - SPACER) // 2  # 90
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        spacer = random.choices(ALPHA, k=SPACER)
        rc = [COMP[c] for c in reversed(half)]
        seq = "".join(half) + "".join(spacer) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} spacer-pal seqs (half={HALF}, spacer={SPACER}) to {OUT}")
