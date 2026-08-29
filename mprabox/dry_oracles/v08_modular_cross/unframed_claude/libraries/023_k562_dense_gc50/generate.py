"""Dense K562 motifs at matched GC=50/50 (exp 005 design, doubled density).

Exp 005 (8 motifs/seq, GC=50/50) gave K562=+0.0077, HepG2=+0.0056,
SKNSH=-0.0003 → mean=+0.0043. The GC-matched null kept HepG2 positive.
Hypothesis: doubling motif density (8→16) should lift K562 above +0.008
while preserving HepG2.

25k active: GC=50, 16 K562 motifs.
25k null: GC=50, no motifs.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

K562_MOTIFS = [
    "AGATAA", "TGATAG", "AGATAG", "TGATAA",
    "CACCC", "CCACCC", "GGGGTG",
    "TGCTGAGTCAGCA",
    "CAGCTG", "CATCTG", "CACCTG",
    "TGAGTCA", "TGACTCA",
    "GGAAGT", "CGGAAG",
    "GGGCGGGG", "GGGCGG",
    "CAGTTG", "AACTG",
    "CCAAT", "TGACGTCA", "CACGTG",  # add a few universals
]

rng = np.random.default_rng(1601)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc=0.50):
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
active = bg(half, L, gc=0.50)
active = insert(active, K562_MOTIFS, n_per_seq=16)
null = bg(N_TOTAL - half, L, gc=0.50)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k K562 16motifs GC50 + 25k null GC50)")
