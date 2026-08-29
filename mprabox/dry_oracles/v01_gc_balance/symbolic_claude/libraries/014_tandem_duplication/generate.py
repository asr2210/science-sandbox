"""
Experiment 014: Tandem duplication (control for exp 012 palindromes).

50K sequences of length 200. Each:
  first 100 chars iid uniform over {0,1,2,3}
  next 100 chars = COPY of first 100 (tandem repeat)

Tests whether the eval_01 lift in exp 012 was specifically due to
reverse-complement symmetry, or whether any half-to-half deterministic
structure suffices. Tandem matches exp 012 in:
  - per-position composition (uniform)
  - deterministic half-to-half coupling
differs only in the relation (identity vs RC).

Prediction:
  if eval_01 ≈ 0.572 → any redundancy works (RC not special)
  if eval_01 < 0.572 → RC specifically matters (biological signal)
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        seq = "".join(half) + "".join(half)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} tandem-duplicated sequences of length {L} to {OUT}")
