"""Experiment 004 — Cell-type-targeted cocktail @ 8 inserts/seq.

Theory v3 says density should stay moderate (~8/seq). Theory v2 says
each cell type wants specific motifs. So: include motifs for ALL
three cell types in each sequence.

Motif palette (length 6-13):
  K562 / erythroid:   AGATAAG (GATA1), CCACGCCC (KLF1), CAGCTG (TAL1/E-box)
  HepG2 / liver:      AGGTCAAAGGTCA (HNF4), GTTAATNATTAAC -> GTTAATGATTAAC (HNF1),
                      TTGCGCAAT (C/EBP), TGTTTGY -> TGTTTGC (FOXA)
  SK-N-SH / neuronal: CACCTG (NEUROD-Ebox), CTATAAATAG (MEF2),
                      ATGCATAATAAA (BRN2/POU3F2)
  Universal:          TGAGTCA (AP-1), TGACGTCA (CRE)
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(4)
N, L = 50_000, 200
bases = np.array(list("ACGT"))

MOTIFS = [
    # K562 / erythroid
    "AGATAAG", "CCACGCCC", "CAGCTG",
    # HepG2 / liver
    "AGGTCAAAGGTCA", "GTTAATGATTAAC", "TTGCGCAAT", "TGTTTGC",
    # SK-N-SH / neuronal
    "CACCTG", "CTATAAATAG", "ATGCATAATAAA",
    # Universal
    "TGAGTCA", "TGACGTCA",
]
INSERTS_PER_SEQ = 8

def gen_one():
    s = list(bases[rng.integers(0, 4, size=L)])
    chosen = rng.choice(len(MOTIFS), size=INSERTS_PER_SEQ, replace=True)
    used = []
    for mi in chosen:
        m = MOTIFS[mi]
        for _ in range(40):
            pos = int(rng.integers(0, L - len(m) + 1))
            ok = all(not (pos < e and pos + len(m) > st) for (st, e) in used)
            if ok:
                used.append((pos, pos + len(m)))
                for j, ch in enumerate(m):
                    s[pos + j] = ch
                break
    return "".join(s)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for _ in range(N):
        f.write(gen_one()); f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
