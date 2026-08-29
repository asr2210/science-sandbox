"""Experiment 007: 3 random motifs at random positions per sequence.

Same motif pool as exp 006; each seq gets 3 motifs placed at random
non-overlapping positions.

Hypothesis (T4): more motif content → bigger improvements on motif-rewarding
evals (07, 13), possibly small drop on flat ones if cumulative variance
loss kicks in. Net eval_01 expected to rise slightly above 0.331.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
N_MOTIFS_PER_SEQ = 3
SEED = 47

MOTIFS = [
    "TGAGTCA", "GGGCGG", "GGGACTTTCC", "GATAAG",
    "CAATCT", "TATAAA", "CACGTG", "TTGCGCAA",
]
MOTIF_ARRS = [np.array(list(m)) for m in MOTIFS]
MAX_MLEN = max(len(m) for m in MOTIFS)

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]

for i in range(N_SEQ):
    used_ranges = []
    placed = 0
    attempts = 0
    while placed < N_MOTIFS_PER_SEQ and attempts < 50:
        attempts += 1
        m_idx = rng.integers(0, len(MOTIFS))
        motif = MOTIF_ARRS[m_idx]
        mlen = len(motif)
        pos = rng.integers(0, LEN - mlen + 1)
        end = pos + mlen
        # check overlap
        ok = all(end <= s or pos >= e for s, e in used_ranges)
        if not ok:
            continue
        mat[i, pos:end] = motif
        used_ranges.append((pos, end))
        placed += 1

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs x {LEN}bp; {N_MOTIFS_PER_SEQ} motifs each, random pos/id")
