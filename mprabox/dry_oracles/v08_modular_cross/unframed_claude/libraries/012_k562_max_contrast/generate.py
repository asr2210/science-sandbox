"""Aggressive K562 maximization: very dense motifs + extreme contrast.

25k active: GC=65%, 12 K562-relevant + universal motifs per 200bp.
25k null: GC=25%, no motifs.

Combines:
- Dense motif insertion (was the only signal that worked)
- High GC contrast between active and null (worked in exp 003)
- Focused K562 motif panel + AP-1/SP1 (universal activators)
"""
import numpy as np
from pathlib import Path
import random

N_TOTAL = 50_000
L = 200

K562_MOTIFS = [
    "AGATAA", "TGATAA", "AGATAG", "TGATAG",       # GATA1 variants
    "CACCC", "GGGGTG", "GGGTGGGG",                # KLF1
    "TGCTGAGTCAGCA",                              # NFE2
    "CAGCTG", "CATCTG", "CACCTG",                 # TAL1 / E-box
    "TGAGTCA", "TGACTCA",                         # AP-1 universal
    "GGGCGG", "GGGCGGGG",                         # SP1
    "GGAAGT", "CGGAAG",                           # ETS
    "CCAAT",                                      # NF-Y
    "TGACGTCA",                                   # CREB
    "CACGTG",                                     # MYC E-box
]

rng = np.random.default_rng(501)
py_rng = random.Random(501)
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
active = bg(half, L, gc=0.65)
active = insert(active, K562_MOTIFS, n_per_seq=12)

null = bg(N_TOTAL - half, L, gc=0.25)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k K562-saturated GC65 + 25k null GC25)")
