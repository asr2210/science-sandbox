"""
Experiment 018: Multi-palindrome (4 x 50bp blocks).

Each sequence = 4 length-50 palindromes concatenated.
Each block: 25 random chars + their RC.
No global RC symmetry; 4 independent local palindromes.

Tests whether the model prefers many short TF-site-scale palindromes
over one long palindrome.
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

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        parts = []
        for _ in range(N_BLOCKS):
            half = random.choices(ALPHA, k=HALF_BLOCK)
            rc = [COMP[c] for c in reversed(half)]
            parts.append("".join(half) + "".join(rc))
        seq = "".join(parts)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} multi-palindrome seqs ({N_BLOCKS}x{BLOCK}bp) to {OUT}")
