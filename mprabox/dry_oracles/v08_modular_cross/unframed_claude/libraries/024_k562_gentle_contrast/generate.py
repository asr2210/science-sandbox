"""Exp 005 design + gentle GC contrast (60/40).

Hypothesis: GC=50/50 (exp 005) gave K562=+0.0077, HepG2=+0.0056.
GC=65/25 (exp 012) gave K562=+0.0089, HepG2=+0.0011.
Try the midpoint GC=60/40: K562 ≈ +0.0082, HepG2 ≈ +0.0035?

25k active: GC=60, 8 K562 motifs (exp 005 panel).
25k null: GC=40, no motifs.
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
]

rng = np.random.default_rng(1701)
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
active = bg(half, L, gc=0.60)
active = insert(active, K562_MOTIFS, n_per_seq=8)
null = bg(N_TOTAL - half, L, gc=0.40)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k K562 8motifs GC60 + 25k null GC40)")
