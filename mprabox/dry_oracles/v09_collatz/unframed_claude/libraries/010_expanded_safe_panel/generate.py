"""Experiment 010: expand 002 panel with known-strong additions.

Add TATAAA (TATA box, classical promoter element) and GGGCGG (canonical
SP1 short form) to 002's safe 10-motif panel. 12 total, density 6, 50% GC
backbone.

Hypothesis: more diversity from proven additions beats 002.
"""
import numpy as np

rng = np.random.default_rng(10)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

MOTIFS = [
    # 002 panel
    "TGAGTCA",       # AP-1
    "TGACGTCA",      # CRE
    "GGGGCGGGG",     # SP1 long
    "ACAGGAAGT",     # ETS
    "CCAATCG",       # CCAAT/NFY
    "CAAAGGTCA",     # HNF4
    "GTTAATCATTAAC", # HNF1
    "AGATAAG",       # GATA1
    "CACCC",         # KLF1
    "CAGCTG",        # E-box
    # additions (known strong, not in 003 suspect set)
    "TATAAA",        # TATA box (classical core promoter)
    "GGGCGG",        # SP1 short (canonical 6-mer)
]
MOTIFS_PER_SEQ = 6

with open("libraries/010_expanded_safe_panel/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = list(BASES[rng.integers(0, 4, size=L)])
        chosen = rng.choice(len(MOTIFS), size=MOTIFS_PER_SEQ, replace=True)
        used = []
        for mi in chosen:
            m = MOTIFS[mi]
            ml = len(m)
            for _try in range(20):
                pos = int(rng.integers(0, L - ml + 1))
                if all(pos + ml <= s or pos >= e for s, e in used):
                    used.append((pos, pos + ml))
                    for j, ch in enumerate(m):
                        seq[pos + j] = ch
                    break
        f.write("".join(seq) + "\n")

print(f"wrote {N} seqs from {len(MOTIFS)}-panel @ d={MOTIFS_PER_SEQ}")
