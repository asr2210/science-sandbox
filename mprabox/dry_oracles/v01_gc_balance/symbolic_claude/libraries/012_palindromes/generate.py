"""
Experiment 012: Palindromic sequences (reverse-complement symmetric).

50K sequences of length 200. Each sequence:
  first 100 chars = random uniform
  next 100 chars  = reverse-complement of first 100

Reverse-complement mapping: A↔T (0↔3), C↔G (1↔2).

Tests whether the model rewards palindromic structure (common in
transcription factor binding sites).
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"

COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        rc = [COMP[c] for c in reversed(half)]
        seq = "".join(half) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} palindromic sequences of length {L} to {OUT}")
