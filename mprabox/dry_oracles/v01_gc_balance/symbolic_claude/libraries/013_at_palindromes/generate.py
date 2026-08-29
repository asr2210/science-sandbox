"""
Experiment 013: AT-rich palindromes (combine palindromes + AT-bias).

50K sequences of length 200. Each:
  first 100 chars iid with P(A)=P(T)=0.30, P(C)=P(G)=0.20
  next 100 chars = reverse-complement of first 100
Composition: 30/20/20/30 (60% AT). Palindromic structure preserved.

Combines two confirmed lifts: palindrome (exp 012) and AT-bias (exp 007).
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"
WEIGHTS = [0.30, 0.20, 0.20, 0.30]  # A C G T
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, weights=WEIGHTS, k=HALF)
        rc = [COMP[c] for c in reversed(half)]
        seq = "".join(half) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} AT-rich palindromes of length {L} to {OUT}")
