"""Experiment 007 — Bipartite GC architecture.

100bp AT-rich half (30% GC) on the left, 100bp GC-rich half (70% GC)
on the right. Embed HepG2-favored AT-rich motifs in the AT half
(HNF1, FOXA, CEBP, MEF2, BRN2) and K562-favored GC-rich motifs in
the GC half (KLF1/SP1, AP-1, E-box). Global GC ~50% to keep SKNSH.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(7)
N, L = 50_000, 200
HALF = L // 2
bases = np.array(list("ACGT"))

AT_PROBS = np.array([0.35, 0.15, 0.15, 0.35])  # 30% GC
GC_PROBS = np.array([0.15, 0.35, 0.35, 0.15])  # 70% GC

AT_MOTIFS = [
    "GTTAATGATTAAC",  # HNF1
    "TGTTTGC",        # FOXA
    "ATTGCGCAAT",     # C/EBP
    "CTATAAATAG",     # MEF2
    "ATGCATAATAAA",   # BRN2
    "TGAGTCA",        # AP-1 (universal)
]

GC_MOTIFS = [
    "CCACGCCCAC",    # KLF1
    "GGGCGGGGC",     # SP1
    "TGAGTCA",       # AP-1 (universal)
    "CACGTG",        # E-box
    "CCAATCG",       # CCAAT-like
    "ACAGGAAGT",     # ETS
]

INSERTS_PER_HALF = 3  # ~3 inserts per half = 6 per sequence total

def gen_half(probs, motifs, half_len):
    s = list(bases[rng.choice(4, size=half_len, p=probs)])
    chosen = rng.choice(len(motifs), size=INSERTS_PER_HALF, replace=True)
    used = []
    for mi in chosen:
        m = motifs[mi]
        if len(m) > half_len:
            continue
        for _ in range(40):
            pos = int(rng.integers(0, half_len - len(m) + 1))
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
        left = gen_half(AT_PROBS, AT_MOTIFS, HALF)
        right = gen_half(GC_PROBS, GC_MOTIFS, HALF)
        f.write(left + right); f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
