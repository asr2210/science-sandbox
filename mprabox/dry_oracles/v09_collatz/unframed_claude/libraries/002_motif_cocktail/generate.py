"""Experiment 002 — Strong activator TF motif cocktail.

Tests theory v1: that mean_r is mean predicted activity per cell type.
Embeds 8 strong universal activator motifs at random non-overlapping
positions in 200bp of random ACGT background.

Motifs chosen: classic strong activators known to boost MPRA output:
  AP-1 / TRE  : TGAGTCA
  CRE         : TGACGTCA
  ETS (core)  : ACAGGAAGT
  E-box (MYC) : CACGTG
  SP1         : GGGCGGGGC
  KLF / GC    : CCACGCCCAC
  GATA        : AGATAAGA
  NFY / CCAAT : ATTGGCTAAT  (CCAAT box context)
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(2)
N, L = 50_000, 200
bases = np.array(list("ACGT"))

MOTIFS = [
    "TGAGTCA",       # AP-1
    "TGACGTCA",      # CRE
    "ACAGGAAGT",     # ETS extended
    "CACGTG",        # E-box (MYC/MAX)
    "GGGCGGGGC",     # SP1
    "CCACGCCCAC",    # KLF
    "AGATAAGA",      # GATA
    "ATTGGCTAAT",    # NFY/CCAAT
]
INSERTS_PER_SEQ = 8

def gen_one():
    # start with random background
    s = list(bases[rng.integers(0, 4, size=L)])
    # pick motifs (with replacement) and random non-overlapping positions
    chosen = rng.choice(len(MOTIFS), size=INSERTS_PER_SEQ, replace=True)
    used = []  # list of (start, end) intervals
    for mi in chosen:
        m = MOTIFS[mi]
        for _ in range(30):  # try positions
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
    for i in range(N):
        f.write(gen_one())
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
