"""Experiment 002: motif-stuffed library.

Insert a panel of strong cis-regulatory motifs at random positions in
random backbone. If the scoring function rewards motif content, we
expect a substantial jump over the 0.231 baseline.

Motif panel (consensus, both strands inserted as forward only since
TF motifs in MPRA models are typically scanned both strands):
  AP-1     TGAGTCA       general enhancer
  CRE      TGACGTCA      general enhancer
  SP1      GGGGCGGGG     promoter
  ETS      ACAGGAAGT     general
  NFY/CCAAT CCAATCG      promoter
  HNF4     CAAAGGTCA     HepG2-specific
  HNF1     GTTAATCATTAAC HepG2-specific
  GATA1    AGATAAG       K562-specific
  KLF1/EKLF CACCC         K562-specific (Sp/KLF box)
  EBOX     CAGCTG         neuronal (NeuroD/ASCL1)
"""
import numpy as np

rng = np.random.default_rng(2)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

MOTIFS = [
    "TGAGTCA",
    "TGACGTCA",
    "GGGGCGGGG",
    "ACAGGAAGT",
    "CCAATCG",
    "CAAAGGTCA",
    "GTTAATCATTAAC",
    "AGATAAG",
    "CACCC",
    "CAGCTG",
]

# Place ~6 motifs per sequence, non-overlapping, random positions and identities.
MOTIFS_PER_SEQ = 6

with open("libraries/002_motif_stuffed/sequences_0.txt", "w") as f:
    for _ in range(N):
        # start with uniform random backbone
        seq = list(BASES[rng.integers(0, 4, size=L)])
        # pick motifs
        chosen = rng.choice(len(MOTIFS), size=MOTIFS_PER_SEQ, replace=True)
        used = []  # list of (start, end) intervals
        for mi in chosen:
            m = MOTIFS[mi]
            ml = len(m)
            for _try in range(20):
                pos = rng.integers(0, L - ml + 1)
                if all(pos + ml <= s or pos >= e for s, e in used):
                    used.append((pos, pos + ml))
                    for j, ch in enumerate(m):
                        seq[pos + j] = ch
                    break
        f.write("".join(seq) + "\n")

print(f"wrote {N} sequences of length {L} with {MOTIFS_PER_SEQ} motifs each")
