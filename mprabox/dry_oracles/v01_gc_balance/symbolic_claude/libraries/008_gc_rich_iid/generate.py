"""
Experiment 008: GC-rich iid (mirror of exp 007).

50K iid per-position sequences with weights {A=0:0.20, C=1:0.30,
G=2:0.30, T=3:0.20}. GC content ~60%. No dinucleotide structure.

Mirror of exp 007 along the GC↔AT composition axis to test symmetry.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"
WEIGHTS = [0.20, 0.30, 0.30, 0.20]  # A C G T

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        f.write("".join(random.choices(ALPHA, weights=WEIGHTS, k=L)))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
