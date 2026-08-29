"""Four-bank library with cell-type-specific motifs.

Bank 1 (K562):  GC-rich, GATA1/KLF/NFE2/TAL1/AP-1 motifs
Bank 2 (HepG2): AT-rich, HNF1A/HNF4A/CEBPA/FOXA motifs
Bank 3 (SKNSH): neutral, NEUROD/ASCL1/CREB/POU3F2 motifs
Bank 4 (null):  low-complexity AT-rich, no motifs

Predict: K562_r, HepG2_r, SKNSH_r all positive simultaneously
because each cell-type model sees its own bank as "active" and
the other banks + null as "less active".
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
L = 200
SEED = 42

K562_MOTIFS = [
    "AGATAA", "TGATAG",        # GATA1 (WGATAR)
    "CACCC", "GGGGTGGGG",      # KLF1
    "TGCTGAGTCAGCA",           # NFE2 (MAF/AP-1 chimera)
    "CAGCTG", "CATCTG",        # TAL1 E-box
    "TGAGTCA", "TGACTCA",      # AP-1
]
HEPG2_MOTIFS = [
    "GTTAATAATTAAC",           # HNF1A
    "AGGTCAAAGGTCA",           # HNF4A DR1
    "TTGCGCAAT", "TTGCGTAAT",  # CEBPA
    "TGTTTAC", "TGTTTGT",      # FOXA1
    "AGGTCA",                  # NR half-site
]
SKNSH_MOTIFS = [
    "CAGCTG", "CACCTG",        # ASCL1 E-box
    "CAGATG", "CATATG",        # NEUROD1
    "TGACGTCA",                # CREB
    "ATGCATAT",                # POU3F2
    "TAATTA", "TAATCA",        # LHX2 homeobox
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")

def gc_bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)

def insert_motifs(seqs, motifs, n_per_seq):
    n = seqs.shape[0]
    for i in range(n):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            pos = rng.integers(0, seqs.shape[1] - len(m) + 1)
            seqs[i, pos:pos + len(m)] = list(m)
    return seqs

N_PER_BANK = N_TOTAL // 4  # 12500

k562 = gc_bg(N_PER_BANK, L, gc=0.60)
k562 = insert_motifs(k562, K562_MOTIFS, n_per_seq=6)

hepg2 = gc_bg(N_PER_BANK, L, gc=0.35)
hepg2 = insert_motifs(hepg2, HEPG2_MOTIFS, n_per_seq=6)

sknsh = gc_bg(N_PER_BANK, L, gc=0.50)
sknsh = insert_motifs(sknsh, SKNSH_MOTIFS, n_per_seq=6)

null = gc_bg(N_PER_BANK, L, gc=0.20)
# Make null even more "null" — long AT runs, no motifs
# (No motif insertion.)

combined = np.concatenate([k562, hepg2, sknsh, null], axis=0)
order = rng.permutation(combined.shape[0])
combined = combined[order]

lines = ["".join(row) for row in combined]
out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {combined.shape[0]} sequences: 4 banks of {N_PER_BANK}")
