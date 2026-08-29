"""Random baseline: 50k uniformly random 200bp DNA sequences."""
import os
import random

random.seed(42)
ALPHABET = "ACGT"
N_SEQS = 50000
LENGTH = 200

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N_SEQS):
        f.write("".join(random.choices(ALPHABET, k=LENGTH)) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
