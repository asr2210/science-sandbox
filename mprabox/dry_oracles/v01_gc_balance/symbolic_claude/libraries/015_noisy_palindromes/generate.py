"""
Experiment 015: Noisy (imperfect) palindromes.

Like exp 012 but with random mismatches in the second half.
For each sequence:
  first 100 chars iid uniform over {0,1,2,3}
  second 100 chars = RC of first half, with each position
    independently re-randomized (to any non-RC char) with p=0.10.

Tests how rigidly the model requires RC symmetry. 10% mismatch
breaks ~10% of positions; if model is rigid, expect noticeable
drop from 0.572; if tolerant, score should be near 0.572.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
P_MUT = 0.10

random.seed(20260603)

def other_char(c):
    return random.choice([x for x in ALPHA if x != c])

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        rc = [COMP[c] for c in reversed(half)]
        # mutate each rc position with prob P_MUT
        for i in range(HALF):
            if random.random() < P_MUT:
                rc[i] = other_char(rc[i])
        seq = "".join(half) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} noisy palindromes (p_mut={P_MUT}) of length {L} to {OUT}")
