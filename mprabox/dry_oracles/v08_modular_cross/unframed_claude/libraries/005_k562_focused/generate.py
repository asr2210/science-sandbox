"""K562-focused 50/50 library at matched GC content.

Isolates motif effect from composition: both halves at GC=50%.
- 25k active: dense K562 motifs (GATA1, KLF, NFE2, TAL1, AP-1, ETS, SP1, MYB)
- 25k null:  GC=50% random, no inserted motifs

Predict: K562_r jumps above +0.02 (matching or exceeding exp 003).
HepG2 and SKNSH should be near zero (no cell-type contamination from
GC contrast).
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200
SEED = 42

# Strong K562 motif panel
MOTIFS = [
    "AGATAA", "TGATAG", "AGATAG", "TGATAA",   # GATA1 variants
    "CACCC", "CCACCC", "GGGGTG",              # KLF1
    "TGCTGAGTCAGCA",                          # NFE2
    "CAGCTG", "CATCTG", "CACCTG",             # TAL1 E-box
    "TGAGTCA", "TGACTCA",                     # AP-1
    "GGAAGT", "CGGAAG",                       # ETS family
    "GGGCGGGG", "GGGCGG",                     # SP1
    "CAGTTG", "AACTG",                        # MYB
]

rng = np.random.default_rng(42)
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
            pos = rng.integers(0, seqs.shape[1] - len(m) + 1)
            seqs[i, pos:pos + len(m)] = list(m)
    return seqs

half = N_TOTAL // 2
active = bg(half, L, gc=0.50)
active = insert(active, MOTIFS, n_per_seq=8)

null = bg(N_TOTAL - half, L, gc=0.50)
# no motif insertion

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]

out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k K562-active GC50 + 25k null GC50)")
