"""Experiment 003: 50k identical random sequences (degeneracy control).

Generate one 200bp random sequence and replicate 50,000 times. Tests
whether prepare.py is sensitive to LIBRARY diversity:
- If score ≈ baseline → prepare.py barely uses individual sequences.
- If score collapses → per-sequence variation matters.
"""
import os
import numpy as np

N_SEQ = 50_000
LENGTH = 200
ALPHA = np.array(list("ACGT"))

rng = np.random.default_rng(3)
single = ALPHA[rng.integers(0, 4, size=LENGTH, dtype=np.uint8)]
seq = "".join(single)
print("Single sequence:", seq)

lines = [seq] * N_SEQ
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines))
    f.write("\n")
print(f"Wrote {N_SEQ} identical sequences")
