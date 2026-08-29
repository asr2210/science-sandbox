"""Reproduce exp 012 (best) with new seed.

Tests if +0.0045 is a hard ceiling or noisy plateau. Same panel + GC,
just different seed.

Active: GC=65%, 12 K562/universal motifs (exp 012 panel exactly).
Null: GC=25%.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

K562_MOTIFS = [
    "AGATAA", "TGATAA", "AGATAG", "TGATAG",
    "CACCC", "GGGGTG", "GGGTGGGG",
    "TGCTGAGTCAGCA",
    "CAGCTG", "CATCTG", "CACCTG",
    "TGAGTCA", "TGACTCA",
    "GGGCGG", "GGGCGGGG",
    "GGAAGT", "CGGAAG",
    "CCAAT",
    "TGACGTCA",
    "CACGTG",
]

rng = np.random.default_rng(2101)  # different seed from exp 012's 501
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
active = insert(active, K562_MOTIFS, n_per_seq=12)
null = bg(N_TOTAL - half, L, gc=0.25)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (exp 012 re-seed: K562-sat 12motifs GC65 + null GC25)")
