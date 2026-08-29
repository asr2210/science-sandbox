"""Push GC contrast further: GC=70 active + 20 all-cell motifs vs GC=15 null.

Exp 012 hit +0.0045 with GC=65/25 contrast + 12 K562 motifs.
Hypothesis: more contrast + broader motif coverage extends the lift.

Active: GC=70%, 20 motifs (K562 + HepG2 + SKNSH + universal), overlap OK.
Null: GC=15%, no motifs.
"""
import numpy as np
from pathlib import Path
import random

N_TOTAL = 50_000
L = 200

ALL_MOTIFS = [
    # Universal
    "TGAGTCA", "TGACTCA",        # AP-1
    "GGGCGG", "GGGCGGGG",        # SP1
    "CCAAT", "CCAATCA",          # NF-Y
    "TGACGTCA",                  # CREB
    "GGAAGT", "CGGAAG",          # ETS
    "CACGTG",                    # MYC E-box
    # K562
    "AGATAA", "TGATAA", "AGATAG", # GATA1
    "CACCC", "GGGGTG",            # KLF1
    "TGCTGAGTCAGCA",              # NFE2
    "CAGCTG", "CATCTG",           # TAL1 / E-box
    # HepG2
    "AGGTCA",                    # NR half-site
    "TTGCGCAAT",                 # CEBPA
    "TGTTTAC", "TGTTTGC",        # FOXA1
    "GTTAATNATTAAC",             # HNF1A
    "TGCCAA",                    # HNF4A half
    # SKNSH
    "CAGATG", "CAGCTG",          # NEUROD / ASCL1
    "TAATTA", "TAATT",           # homeobox
    "ATGCAT",                    # POU
    "CAGGTG",                    # E-box (NEUROD-like)
]

rng = np.random.default_rng(1001)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGTN", "TGCAN")


def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            # Replace any N in motif with random base
            if "N" in m:
                m = "".join(rng.choice(list("ACGT")) if c == "N" else c for c in m)
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            if ml > seqs.shape[1]:
                continue
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


half = N_TOTAL // 2
active = bg(half, L, gc=0.70)
active = insert(active, ALL_MOTIFS, n_per_seq=20)

null = bg(N_TOTAL - half, L, gc=0.15)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k all-cell-saturated GC70 + 25k null GC15)")
print(f"Active GC: {(active == 'C').sum() / active.size + (active == 'G').sum() / active.size:.3f}")
print(f"Null GC: {(null == 'C').sum() / null.size + (null == 'G').sum() / null.size:.3f}")
