"""Experiment 008: Random uniform with a different seed.

Measures noise floor — same distribution as exp 001 but different RNG seed.
If score ≈ 0.32 ± small, uniform random is reproducibly the ceiling for
"composition + simple insertion" strategies.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(987654321)  # different seed than 001
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
seqs = ["".join(ALPHABET[row]) for row in idx]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} uniform random sequences (seed=987654321) to {out_path}")
