"""
Experiment 023: Many TFBS-scale short palindromes in random background.

K=15 palindromes of length 6bp inserted at random non-overlapping
positions in 200bp uniform random background.
Total palindromic content: 90bp distributed as 15 tiny TFBS-like motifs.

Tests whether the model recognizes biological TF-binding-site-scale
palindromic motifs (real TFBS are typically 6-12bp).
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
K = 15
PAL_LEN = 6
PAL_HALF = PAL_LEN // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)


def random_pal(half_len):
    half = random.choices(ALPHA, k=half_len)
    rc = [COMP[c] for c in reversed(half)]
    return half + rc


def pick_positions(seq_len, k, motif_len):
    """Pick k non-overlapping starts for length-motif_len motifs."""
    free = list(range(seq_len - motif_len + 1))
    chosen = []
    # greedy: sample, remove conflicting positions, repeat
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

print(f"Wrote {N} sparse-tinypal seqs (K={K} x {PAL_LEN}bp) to {OUT}")
