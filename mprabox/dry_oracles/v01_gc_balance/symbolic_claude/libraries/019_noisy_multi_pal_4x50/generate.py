"""
Experiment 019: Noisy multi-palindrome (4 x 50bp, p=0.10 per block).

Combines two prior winners:
  - noisy palindromes (p=0.10 mismatches in RC half) - exp 015 (best 0.5801)
  - multi-palindrome (4x50bp blocks) - exp 018 (0.5725)

Each block: 25 random chars + RC with each position mutated p=0.10.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
BLOCK = 50
HALF_BLOCK = BLOCK // 2
N_BLOCKS = L // BLOCK
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
P_MUT = 0.10

random.seed(20260603)

def other_char(c):
    return random.choice([x for x in ALPHA if x != c])

with open(OUT, "w") as f:
    for _ in range(N):
        parts = []
        for _ in range(N_BLOCKS):
            half = random.choices(ALPHA, k=HALF_BLOCK)
            rc = [COMP[c] for c in reversed(half)]
            for i in range(HALF_BLOCK):
                if random.random() < P_MUT:
                    rc[i] = other_char(rc[i])
            parts.append("".join(half) + "".join(rc))
        seq = "".join(parts)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} noisy multi-pal ({N_BLOCKS}x{BLOCK}bp, p_mut={P_MUT}) to {OUT}")
