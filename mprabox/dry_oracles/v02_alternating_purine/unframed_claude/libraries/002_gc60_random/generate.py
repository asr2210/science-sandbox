"""GC-rich random sequences (60% GC)."""
import os, random

random.seed(2)
N_SEQS, LENGTH = 50000, 200
# probabilities: A=0.20, T=0.20, C=0.30, G=0.30
ALPHABET = ["A", "C", "G", "T"]
WEIGHTS = [0.20, 0.30, 0.30, 0.20]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N_SEQS):
        f.write("".join(random.choices(ALPHABET, weights=WEIGHTS, k=LENGTH)) + "\n")
print(f"Wrote {N_SEQS} sequences (GC=0.6)")
