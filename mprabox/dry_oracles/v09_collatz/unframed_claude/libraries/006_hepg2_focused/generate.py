"""Experiment 006: HepG2-focused library.

Goal: push HepG2_r from 0.04 to as high as possible while not destroying
SK-N-SH (which is currently the dominant contributor at 0.63).

Design: 6 motifs per sequence drawn from a HepG2-skewed panel. Keep
universal activators (AP-1, CRE, ETS) which 002 showed are safe; add
hepatocyte-specific HNF4, HNF1, FOXA1; weight HNF4/HNF1 heavily.
Avoid the suspect set from 003 (TAL1, CEBPA, ZIC, RUNX1, NRF1).
"""
import numpy as np

rng = np.random.default_rng(6)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

# (motif, weight) — higher weight = picked more often
PANEL = [
    ("CAAAGGTCA",    3.0),   # HNF4α — primary HepG2 TF
    ("GTTAATCATTAAC",3.0),   # HNF1α — primary HepG2 TF
    ("TGTTTGC",      2.0),   # FOXA1/2 — pioneer hepatic TF
    ("TGAGTCA",      1.5),   # AP-1 — universal
    ("TGACGTCA",     1.5),   # CRE — universal
    ("ACAGGAAGT",    1.0),   # ETS — universal
    ("CCAATCG",      1.0),   # CCAAT/NFY — universal promoter
    ("GGGGCGGGG",    1.0),   # SP1 — universal promoter
    ("CAGCTG",       0.5),   # E-box — keep for SK-N-SH support
    ("AGATAAG",      0.5),   # GATA1 — keep some K562 support
    ("CACCC",        0.5),   # KLF1 — keep some K562 support
]
motifs   = [m for m, _ in PANEL]
weights  = np.array([w for _, w in PANEL])
probs    = weights / weights.sum()

MOTIFS_PER_SEQ = 6

with open("libraries/006_hepg2_focused/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = list(BASES[rng.integers(0, 4, size=L)])
        chosen = rng.choice(len(motifs), size=MOTIFS_PER_SEQ, replace=True, p=probs)
        used = []
        for mi in chosen:
            m = motifs[mi]
            ml = len(m)
            for _try in range(20):
                pos = int(rng.integers(0, L - ml + 1))
                if all(pos + ml <= s or pos >= e for s, e in used):
                    used.append((pos, pos + ml))
                    for j, ch in enumerate(m):
                        seq[pos + j] = ch
                    break
        f.write("".join(seq) + "\n")

print(f"wrote {N} seqs, HepG2-weighted panel, {MOTIFS_PER_SEQ} motifs each")
