"""GC-poor random sequences (40% GC)."""
import os, random

random.seed(3)
N_SEQS, LENGTH = 50000, 200
ALPHABET = ["A", "C", "G", "T"]
WEIGHTS = [0.30, 0.20, 0.20, 0.30]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N_SEQS):
        f.write("".join(random.choices(ALPHABET, weights=WEIGHTS, k=LENGTH)) + "\n")
print(f"Wrote {N_SEQS} sequences (GC=0.4)")
