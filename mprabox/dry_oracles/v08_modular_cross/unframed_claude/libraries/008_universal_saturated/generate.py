"""Saturated universal-motif library, 50/50.

Hypothesis: maximize variance in motif_count(x) by saturating the
active half with universal motifs (recognized by all three cell-line
models) and leaving the null half motif-free. Both halves at GC=50%.

Universal motif panel: AP-1, SP1, NF-Y, CREB, ETS, E-box/MYC, plus
strong cell-specific motifs for cross-coverage (GATA, HNF, NEUROD).
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200
N_MOTIFS_ACTIVE = 14   # ~14 motifs in 200bp

MOTIFS = [
    # Universal / housekeeping
    "TGAGTCA", "TGACTCA",       # AP-1
    "GGGCGGGG", "GGGCGG",       # SP1 GC-box
    "CCAATCA", "CCAAT",         # NF-Y
    "TGACGTCA",                 # CREB
    "GGAAGT", "ACTTCC",         # ETS (fwd and rev manually)
    "CACGTG",                   # E-box / MYC
    # K562-leaning
    "AGATAA", "TGATAA",         # GATA1
    "CACCC",                    # KLF
    # HepG2-leaning (used sparingly)
    "AGGTCA",                   # NR half (broad)
    # SKNSH-leaning
    "CAGCTG", "CAGATG",         # E-box variants
    "TAATTA",                   # homeobox
]

rng = np.random.default_rng(45)
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
            pos = rng.integers(0, seqs.shape[1] - len(m) + 1)
            seqs[i, pos:pos + len(m)] = list(m)
    return seqs

half = N_TOTAL // 2
active = bg(half, L, gc=0.50)
active = insert(active, MOTIFS, n_per_seq=N_MOTIFS_ACTIVE)

null = bg(N_TOTAL - half, L, gc=0.50)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k saturated-active {N_MOTIFS_ACTIVE} motifs + 25k null)")
