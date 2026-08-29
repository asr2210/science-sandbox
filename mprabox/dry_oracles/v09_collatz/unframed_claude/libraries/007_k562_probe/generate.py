"""Experiment 007: K562 probe — does ANY motif move K562?

K562 has been stuck at 0.13 across all libraries. Probe with a panel
focused on erythroid TFs (avoiding suspect motifs from 003).

Panel:
  GATA1 AGATAAG (was good)
  KLF1 CACCC (was good)
  GATA1-KLF composite AGATAAGNNCACCC (erythroid superenhancer-style)
  PU.1 AGGAAGT
  NFE2/MARE TGCTGAGTCAT — try this one (was in 003 but maybe ok)
  Plus universal AP-1, CRE, ETS, SP1 for diversity
6 motifs per seq.
"""
import numpy as np

rng = np.random.default_rng(7)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

PANEL = [
    "AGATAAG",                # GATA1
    "CACCC",                  # KLF1
    "AGATAAGGCCACCC",         # GATA1-KLF1 composite (12bp)
    "AGGAAGT",                # PU.1/SPI1
    "TGCTGAGTCAT",            # NFE2/MARE
    "TGAGTCA",                # AP-1
    "TGACGTCA",               # CRE
    "ACAGGAAGT",              # ETS
    "GGGGCGGGG",              # SP1
]

MOTIFS_PER_SEQ = 6

with open("libraries/007_k562_probe/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = list(BASES[rng.integers(0, 4, size=L)])
        chosen = rng.choice(len(PANEL), size=MOTIFS_PER_SEQ, replace=True)
        used = []
        for mi in chosen:
            m = PANEL[mi]
            ml = len(m)
            for _try in range(20):
                pos = int(rng.integers(0, L - ml + 1))
                if all(pos + ml <= s or pos >= e for s, e in used):
                    used.append((pos, pos + ml))
                    for j, ch in enumerate(m):
                        seq[pos + j] = ch
                    break
        f.write("".join(seq) + "\n")

print(f"wrote {N} seqs with K562 erythroid panel, {MOTIFS_PER_SEQ} motifs each")
