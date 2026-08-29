"""HepG2-focused 50/50 library at matched GC.

Both halves at GC=40% (HepG2-friendly composition). Active half has
dense HNF1A/HNF4A/CEBPA/FOXA/PPAR motifs; null half is plain GC=40%.

Predict: HepG2_r jumps well above +0.01.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

MOTIFS = [
    "GTTAATAATTAAC", "GTTAATGATTAAC",       # HNF1A palindrome
    "AGGTCAAAGGTCA", "AGGTCATAGGTCA",       # HNF4A DR1
    "TTGCGCAAT", "TTGCGTAAT", "TTGCGCAAC",  # CEBPA
    "TGTTTAC", "TGTTTGC", "TGTTTGT",        # FOXA
    "AGGTCA",                                # NR half-site (broad)
    "TGGCAAT", "ATTGCCA",                   # CEBP variants
    "CAAAG", "TCAAAG",                      # FOXA core
]

rng = np.random.default_rng(43)
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
active = bg(half, L, gc=0.40)
active = insert(active, MOTIFS, n_per_seq=8)

null = bg(N_TOTAL - half, L, gc=0.40)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]

lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k HepG2-active GC40 + 25k null GC40)")
