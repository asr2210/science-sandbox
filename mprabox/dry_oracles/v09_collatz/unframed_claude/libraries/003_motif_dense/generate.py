"""Experiment 003 — same cocktail as exp 002 but DENSE.

Doubles motif inserts per sequence (16 vs 8) to test dose response.
If theory is "more motifs = higher score", mean_r should keep climbing.
If saturation or hurt, single-motif/cell-type targeting is needed.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(3)
N, L = 50_000, 200
bases = np.array(list("ACGT"))

MOTIFS = [
    "TGAGTCA", "TGACGTCA", "ACAGGAAGT", "CACGTG",
    "GGGCGGGGC", "CCACGCCCAC", "AGATAAGA", "ATTGGCTAAT",
]
INSERTS_PER_SEQ = 16

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
