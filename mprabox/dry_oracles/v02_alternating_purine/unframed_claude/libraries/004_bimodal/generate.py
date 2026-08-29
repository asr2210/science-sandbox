"""004 — Bimodal library: 25k random + 25k motif-rich.

Hypothesis: if the metric correlates predicted vs true activity per sequence,
then a library with high VARIANCE in activity (mixing low-activity randoms
with high-activity motif-rich seqs) should yield higher correlation than a
uniform library.

If K562_r jumps from ~0.01 to >0.05, hypothesis confirmed.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(4)
N, L = 50_000, 200
HALF = N // 2
ALPH = np.array(list("ACGT"))

# Strong activator motifs from multiple cell types
MOTIFS = [
    "AGATAAG",      # GATA1 (K562)
    "CACCCC",       # KLF1 (K562)
    "CAAAGTCCA",    # HNF4A (HepG2)
    "GTTAATCATTAAC",# HNF1A (HepG2)
    "TTGCGCAAT",    # C/EBP (HepG2)
    "CAGCTG",       # NEUROD bHLH (SKNSH)
    "GGGCGG",       # SP1
    "CCAATG",       # NFY
    "TGACTCA",      # AP-1
    "TGACGTCA",     # CREB
    "TATAAAA",      # TATA
    "CCACGTG",      # E-box
    "GGAAGT",       # ETS
]

lines = []
# Half pure random
for _ in range(HALF):
    seq = ALPH[rng.integers(0, 4, size=L)]
    lines.append("".join(seq))

# Half motif-rich (10 motifs per sequence)
for _ in range(N - HALF):
    arr = list(ALPH[rng.integers(0, 4, size=L)])
    n_ins = 10
    used = set()
    for _ in range(n_ins):
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        # find non-overlapping spot
        for _try in range(20):
            pos = int(rng.integers(0, L - len(m)))
            if all((pos + i) not in used for i in range(len(m))):
                for i, ch in enumerate(m):
                    arr[pos + i] = ch
                    used.add(pos + i)
                break
    lines.append("".join(arr))

rng.shuffle(lines)
out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {N} sequences to {out}")
