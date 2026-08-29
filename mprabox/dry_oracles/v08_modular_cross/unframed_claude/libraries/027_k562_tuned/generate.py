"""Exp 012 tuned: 14 motifs, panel includes HepG2-friendly universals.

Exp 012 base design: GC=65 active + 12 K562 motifs, GC=25 null. +0.0045.
Tweaks:
- 14 motifs/seq (vs 12)
- Added NR half-site (AGGTCA) and stronger CCAAT for HepG2 spillover
- Slightly less extreme null (GC=30) to keep HepG2 alive
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

MOTIFS = [
    # K562-specific (essential for K562 r)
    "AGATAA", "TGATAA", "AGATAG", "TGATAG",       # GATA1
    "CACCC", "GGGGTG", "GGGTGGGG",                # KLF1
    "TGCTGAGTCAGCA",                              # NFE2
    "CAGCTG", "CATCTG", "CACCTG",                 # TAL1 / E-box
    # Universals
    "TGAGTCA", "TGACTCA",                         # AP-1
    "GGGCGG", "GGGCGGGG",                         # SP1
    "GGAAGT", "CGGAAG",                           # ETS
    "CCAAT", "CCAATCA",                           # NF-Y (HepG2 booster)
    "TGACGTCA",                                   # CREB
    "CACGTG",                                     # MYC E-box
    # HepG2 boosters (universal-ish)
    "AGGTCA",                                     # NR half-site (HNF4A-friendly)
    "TGTTTAC",                                    # FOXA-like
]

rng = np.random.default_rng(2001)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


half = N_TOTAL // 2
active = bg(half, L, gc=0.65)
active = insert(active, MOTIFS, n_per_seq=14)
null = bg(N_TOTAL - half, L, gc=0.30)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k K562+HepG2-friendly 14motifs GC65 + 25k null GC30)")
