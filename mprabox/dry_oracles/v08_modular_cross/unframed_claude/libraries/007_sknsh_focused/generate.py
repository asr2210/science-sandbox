"""SKNSH-focused 50/50 library at matched GC=50%.

25k active: GC=50% bg + dense neuronal/E-box motifs (ASCL1, NEUROD,
CREB, POU3F2, LHX2, SOX, MEF2, NFI). 25k null: plain GC=50%.

Predict: SKNSH_r jumps positive. K562/HepG2 should stay near zero.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200

MOTIFS = [
    "CAGCTG", "CACCTG", "CACGTG",       # E-box variants (ASCL1, NEUROD, MYC)
    "CAGATG", "CATATG",                 # NEUROD1
    "TGACGTCA",                         # CREB
    "ATGCATAT", "ATGCAAAT",             # POU3F2 (Brn2)
    "TAATTA", "TAATCA",                 # LHX2 homeobox
    "CATTGT", "ACAAT",                  # SOX
    "CTATTTATAG",                       # MEF2
    "TTGGCA",                           # NFI
    "TGACTCA",                          # AP-1 (also active in neurons)
    "GGGCGG",                           # SP1 (housekeeping)
]

rng = np.random.default_rng(44)
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
active = insert(active, MOTIFS, n_per_seq=8)
null = bg(N_TOTAL - half, L, gc=0.50)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k SKNSH-active + 25k null, GC=50)")
