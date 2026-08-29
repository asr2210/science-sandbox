"""Experiment 008 — Big-4 universal activators only.

Hypothesis: a small set of strongest universal activators
(AP-1, SP1, NFY, CRE) are doing most of the work in exp 002 cocktail.
Test by using only these 4 motifs at 8 inserts/seq.

If mean_r >= exp 002 (0.2541), simpler is better.
If mean_r < exp 002, some of the other motifs were contributing.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(8)
N, L = 50_000, 200
bases = np.array(list("ACGT"))

MOTIFS = [
    "TGAGTCA",       # AP-1
    "TGACGTCA",      # CRE
    "GGGCGGGGC",     # SP1
    "ATTGGCTAATC",   # NFY/CCAAT extended
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
