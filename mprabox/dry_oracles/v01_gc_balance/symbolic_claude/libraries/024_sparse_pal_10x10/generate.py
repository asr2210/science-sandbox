"""
Experiment 024: Sparse palindromes, K=10 x 10bp.

100bp palindromic content distributed as 10 length-10 motifs.
Compare with:
  exp 022: 5x20bp sparse → 0.5794
  exp 023: 15x6bp sparse → 0.5565

Tests whether the peak length is between 6 and 20.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
K = 10
PAL_LEN = 10
PAL_HALF = PAL_LEN // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)


def random_pal(half_len):
    half = random.choices(ALPHA, k=half_len)
    rc = [COMP[c] for c in reversed(half)]
    return half + rc


def pick_positions(seq_len, k, motif_len):
    free = list(range(seq_len - motif_len + 1))
    chosen = []
    for _ in range(k):
        if not free:
            return None
        s = random.choice(free)
        chosen.append(s)
        free = [p for p in free if abs(p - s) >= motif_len]
    return sorted(chosen)


with open(OUT, "w") as f:
    for _ in range(N):
        seq = random.choices(ALPHA, k=L)
        starts = None
        while starts is None:
            starts = pick_positions(L, K, PAL_LEN)
        for s in starts:
            pal = random_pal(PAL_HALF)
            seq[s : s + PAL_LEN] = pal
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sparse-pal (K={K} x {PAL_LEN}bp) to {OUT}")
