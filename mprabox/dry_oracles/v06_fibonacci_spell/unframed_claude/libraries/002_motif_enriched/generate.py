"""Experiment 002: dense canonical TF motifs on random background.

Each 200bp sequence is a random A/C/G/T background with ~8 strong canonical
motifs inserted at non-overlapping random positions. Motifs are drawn from a
pool spanning K562, HepG2, SKNSH and broadly active TFs, plus some reverse-
complement variants.

Purpose: test whether prepare.py rewards per-sequence regulatory activity.
If yes, mean_r should jump well above the random baseline (eval_01=0.1185),
especially for K562 (baseline ~0).
"""
import os
import numpy as np

N_SEQ = 50_000
LENGTH = 200
ALPHA = np.array(list("ACGT"))

# Canonical strong TF motifs (mostly consensus binding sites)
MOTIFS = [
    # Broad activators
    "TGACTCA",      # AP-1
    "TGAGTCA",      # AP-1 alt
    "TGACGTCA",     # CREB
    "CCAAT",        # NFY / CEBP
    "GGGGCGGGG",    # SP1 (GC box)
    "GGGCGGG",      # SP1 short
    # ETS family (broad)
    "ACTTCCTGT",    # ETS / GABPA
    "CAGGAAGT",     # ETS
    "GGAAGT",       # ETS short
    # E-box (broad: MYC, TAL1, etc.)
    "CACGTG",       # MYC E-box
    "CAGCTG",       # TAL1 / E-box
    "CAGGTG",       # E-box variant
    # K562 / erythroid
    "AGATAA",       # GATA1
    "TTATCT",       # GATA1 rev-comp
    "GATAAG",       # GATA shifted
    "CCACACCC",     # KLF1
    "GGGTGTGG",     # KLF1 rc
    # HepG2 / liver
    "CAAAGTCCA",    # HNF4A
    "TGGACTTTG",    # HNF4A rc
    "TGTTTGC",      # FOXA / HNF3
    "GCAAACA",      # FOXA rc
    "TGACCTTTG",    # HNF4 variant
    # SK-N-SH / neural
    "CAGCTG",       # ASCL1 (E-box)
    "CATATG",       # NEUROD-like
    # Misc strong
    "TTTGCATAAC",   # OCT4-like POU
    "ATGCAAAT",     # OCT
    "GGGAATTCCC",   # NF-kB
    "GGGACTTTCC",   # NF-kB alt
]

MOTIFS = [m.upper() for m in MOTIFS]
MOTIF_LENS = np.array([len(m) for m in MOTIFS])

N_INSERTIONS_PER_SEQ = 8  # ~ 8 motifs per 200bp ≈ heavy load

rng = np.random.default_rng(2)

# Background: random ACGT
bg_idx = rng.integers(0, 4, size=(N_SEQ, LENGTH), dtype=np.uint8)
seqs = ALPHA[bg_idx]  # (N_SEQ, LENGTH)

# For each sequence, insert N_INSERTIONS_PER_SEQ motifs at random non-overlap positions
for i in range(N_SEQ):
    chosen = rng.integers(0, len(MOTIFS), size=N_INSERTIONS_PER_SEQ)
    # pick non-overlapping start positions greedy-style
    used = np.zeros(LENGTH, dtype=bool)
    for m_idx in chosen:
        m = MOTIFS[m_idx]
        L = len(m)
        # try up to 20 random starts
        for _ in range(20):
            start = int(rng.integers(0, LENGTH - L + 1))
            if not used[start:start + L].any():
                # insert
                for j, ch in enumerate(m):
                    seqs[i, start + j] = ch
                used[start:start + L] = True
                break

lines = ["".join(row) for row in seqs]
assert len(lines) == N_SEQ
assert all(len(s) == LENGTH for s in lines)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines))
    f.write("\n")

print(f"Wrote {N_SEQ} sequences with up to {N_INSERTIONS_PER_SEQ} motifs each")
print(f"Sample: {lines[0]}")
