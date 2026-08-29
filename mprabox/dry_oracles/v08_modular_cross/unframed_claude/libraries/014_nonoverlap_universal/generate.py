"""Universal motifs with NON-OVERLAPPING placement.

Fixed earlier issue: random motif insertion overwrote previous motifs.
Now place 12 motifs at non-overlapping positions, randomly chosen.

Each active sequence carries a broad panel mix (K562 + HepG2 + SKNSH +
universal motifs), with reverse-complement diversity. 50/50 with
matched-GC null.
"""
import numpy as np
from pathlib import Path
import random

N_TOTAL = 50_000
L = 200
N_MOTIFS = 12

# Broad universal + cell-rotating motif panel
MOTIFS = [
    # Universal
    "TGAGTCA", "TGACTCA",        # AP-1
    "GGGCGGGG",                  # SP1
    "CCAATCA",                   # NF-Y
    "TGACGTCA",                  # CREB
    "GGAAGT",                    # ETS
    "CACGTG",                    # MYC E-box
    # K562
    "AGATAA", "TGATAA",          # GATA1
    "CACCC",                     # KLF
    "CAGCTG",                    # TAL1 / ASCL1 E-box (shared)
    # HepG2
    "AGGTCA",                    # NR half-site
    "TTGCGCAAT",                 # CEBPA
    "TGTTTAC",                   # FOXA1
    # SKNSH
    "CAGATG",                    # NEUROD
    "TAATTA",                    # homeobox
    "ATGCATAT",                  # POU3F2
]

rng = np.random.default_rng(701)
py_rng = random.Random(702)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")

def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)

def insert_nonoverlap(seq_row, motifs, n):
    """Insert n motifs at non-overlapping random positions in seq_row.
    Returns sequence (numpy 1d array of chars)."""
    L_ = len(seq_row)
    used = []  # list of (start, end)
    for _ in range(n):
        # pick motif
        m = motifs[rng.integers(len(motifs))]
        if rng.random() < 0.5:
            m = m.translate(COMP)[::-1]
        ml = len(m)
        # try random positions until one fits without overlap
        for _try in range(100):
            pos = rng.integers(0, L_ - ml + 1)
            ok = True
            for s, e in used:
                if not (pos + ml <= s or pos >= e):
                    ok = False
                    break
            if ok:
                seq_row[pos:pos + ml] = list(m)
                used.append((pos, pos + ml))
                break
    return seq_row

half = N_TOTAL // 2
active = bg(half, L, gc=0.50)
for i in range(half):
    active[i] = insert_nonoverlap(active[i], MOTIFS, N_MOTIFS)

null = bg(N_TOTAL - half, L, gc=0.50)

combined = np.concatenate([active, null], axis=0)
order = rng.permutation(N_TOTAL)
combined = combined[order]
lines = ["".join(r) for r in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N_TOTAL} (25k non-overlap {N_MOTIFS}-motif active + 25k null GC50)")
