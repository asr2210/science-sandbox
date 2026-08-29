"""5-level continuous gradient of motif density.

Hypothesis: bimodal (saturated active + null) plateaus at +0.0045 because
both predictors saturate at the active extreme. A multi-level gradient
0/3/6/10/18 motifs gives a continuous distribution; if both predictors
track motif count monotonically, Pearson r should beat bimodal.

10k sequences per level, GC=50% throughout (no GC confound). Motifs from
K562 + universal panel (worked best in 012).
"""
import numpy as np
from pathlib import Path

N_PER_LEVEL = 10_000
L = 200
LEVELS = [0, 3, 6, 10, 18]

MOTIFS = [
    # Universal — most robust signals
    "TGAGTCA", "TGACTCA",        # AP-1
    "GGGCGG", "GGGCGGGG",        # SP1
    "CCAAT",                     # NF-Y
    "TGACGTCA",                  # CREB
    "GGAAGT", "CGGAAG",          # ETS
    "CACGTG",                    # MYC E-box
    # K562 (strongest cell-type-specific in exp 012)
    "AGATAA", "TGATAA",          # GATA1
    "CACCC",                     # KLF1
    "CAGCTG", "CATCTG",          # TAL1 / E-box
    "TGCTGAGTCAGCA",             # NFE2
]

rng = np.random.default_rng(1201)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    if n_per_seq == 0:
        return seqs
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            if ml > seqs.shape[1]:
                continue
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


blocks = []
for n_motifs in LEVELS:
    b = bg(N_PER_LEVEL, L, gc=0.50)
    b = insert(b, MOTIFS, n_per_seq=n_motifs)
    blocks.append(b)

combined = np.concatenate(blocks, axis=0)
order = rng.permutation(combined.shape[0])
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {combined.shape[0]} (5x10k gradient: {LEVELS} motifs/seq, GC=50)")
