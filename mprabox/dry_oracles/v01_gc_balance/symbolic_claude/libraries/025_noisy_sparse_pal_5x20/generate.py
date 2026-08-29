"""
Experiment 025: Noisy sparse palindromes (5 x 20bp, p=0.10 noise).

Combines best two designs so far:
  - sparse 5x20bp (exp 022: 0.5794)
  - noisy palindromes (exp 015: 0.5801)

For each block: 10 random + 10 RC, with each RC position mutated p=0.10.
Embedded at 5 random non-overlapping positions in 200bp random background.

Tests whether noise+sparse stacks (most prior combos were sub-additive).
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
K = 5
PAL_LEN = 20
PAL_HALF = PAL_LEN // 2
P_MUT = 0.10
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)


def other_char(c):
    return random.choice([x for x in ALPHA if x != c])


def random_noisy_pal(half_len, p_mut):
    half = random.choices(ALPHA, k=half_len)
    rc = [COMP[c] for c in reversed(half)]
    for i in range(half_len):
        if random.random() < p_mut:
            rc[i] = other_char(rc[i])
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
            seq[s : s + PAL_LEN] = random_noisy_pal(PAL_HALF, P_MUT)
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} noisy-sparse-pal (K={K} x {PAL_LEN}bp, p={P_MUT}) to {OUT}")
