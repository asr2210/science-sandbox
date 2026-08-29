"""
Experiment 007: AT-rich, no dinucleotide structure.

50K sequences, per-position iid with weights matching the stationary
distribution of human DNA under mapping {0,1,2,3}={A,C,G,T}:
  P(A=0)=0.30, P(C=1)=0.20, P(G=2)=0.20, P(T=3)=0.30
AT content ~60%, GC content ~40%. No dinucleotide correlations.

This decouples composition (kept) from dinucleotide structure (removed).
By comparing to exp 006 (full DNA-Markov), we attribute eval_07/13
lifts to composition vs structure.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"
WEIGHTS = [0.30, 0.20, 0.20, 0.30]  # A C G T

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        f.write("".join(random.choices(ALPHA, weights=WEIGHTS, k=L)))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
