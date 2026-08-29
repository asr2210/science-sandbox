"""
Experiment 022: Sparse palindrome insertion in random background.

For each sequence:
  - generate 200bp uniform random background
  - pick K=5 non-overlapping random positions
  - overwrite each with a fresh length-20 palindrome
Total palindromic content: 100bp; the remaining 100bp is random
background flanking the palindromes.

Tests whether the model recognizes embedded TFBS-like palindromes
in a more biologically realistic "random background + motifs" pattern.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
K = 5
PAL_LEN = 20
PAL_HALF = PAL_LEN // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}

random.seed(20260603)


def random_pal(half_len):
    half = random.choices(ALPHA, k=half_len)
    rc = [COMP[c] for c in reversed(half)]
    return half + rc  # list of chars


def pick_positions(seq_len, k, motif_len):
    """Pick k non-overlapping start positions for motifs of length motif_len."""
    while True:
        starts = sorted(random.sample(range(seq_len - motif_len + 1), k))
        ok = all(starts[i + 1] - starts[i] >= motif_len for i in range(k - 1))
        if ok:
            return starts


with open(OUT, "w") as f:
    for _ in range(N):
        seq = random.choices(ALPHA, k=L)
        starts = pick_positions(L, K, PAL_LEN)
        for s in starts:
            pal = random_pal(PAL_HALF)
            seq[s : s + PAL_LEN] = pal
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sparse-pal seqs (K={K} x {PAL_LEN}bp in {L}bp bg) to {OUT}")
