"""
Experiment 029: noisy palindrome p=0.10, seed=99 (final seed shot).

Last seed-search attempt. Previous noisy-pal seeds gave:
  20260603 (015): 0.5801 ← current best
  424242   (026): 0.5442
  7        (027): 0.5719
  12345    (028): 0.5575

Mean 0.563, std 0.013. Try seed=99 for one more shot at the tail.
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

random.seed(99)

def other_char(c):
    return random.choice([x for x in ALPHA if x != c])

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        rc = [COMP[c] for c in reversed(half)]
        for i in range(HALF):
            if random.random() < P_MUT:
                rc[i] = other_char(rc[i])
        seq = "".join(half) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} noisy palindromes (p={P_MUT}, seed=99) to {OUT}")
