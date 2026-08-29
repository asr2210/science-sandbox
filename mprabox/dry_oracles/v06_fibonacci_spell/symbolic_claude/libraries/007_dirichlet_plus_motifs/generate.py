"""Experiment 007: Dirichlet(0.3) base + light motif insertion.

Combines the proven compositional variance (003: 0.135) with motif
insertion (005: 0.123 alone). Tests if motifs add r ON TOP OF
composition. Uses 0->A, 1->C, 2->G, 3->T mapping. Light insertion
(0-5) to preserve compositional variance.

If r > 0.135: motifs help in this mapping; iterate on motif content.
If r ~ 0.135: motifs neutral; try a different mapping or different
              insertion strategy.
"""
import os
import numpy as np

N_SEQS = 50_000
LEN = 200
ALPHA = 0.3
MAX_INSERT = 5
SEED = 41

ENC = {"A": "0", "C": "1", "G": "2", "T": "3"}
def encode(s):
    return "".join(ENC[c] for c in s)

MOTIFS = [encode(m) for m in (
    "TATAAA", "CAGCTG", "GGGCGG", "CCAATC", "TGAGTCA", "TGACGTCA",
    "GGGACTTTCC", "AGATAA", "AGGTCA",
)]

rng = np.random.default_rng(SEED)
chars = np.array(list("0123"))

compositions = rng.dirichlet([ALPHA] * 4, size=N_SEQS)
cum = np.cumsum(compositions, axis=1)
uniforms = rng.random((N_SEQS, LEN))
seqs = np.zeros((N_SEQS, LEN), dtype=np.uint8)
for j in range(LEN):
    seqs[:, j] = (uniforms[:, j:j+1] > cum[:, :3]).sum(axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N_SEQS):
        s = list(chars[seqs[i]])
        n_ins = int(rng.integers(0, MAX_INSERT + 1))
        for _ in range(n_ins):
            m = MOTIFS[rng.integers(0, len(MOTIFS))]
            pos = int(rng.integers(0, LEN - len(m) + 1))
            for k, ch in enumerate(m):
                s[pos + k] = ch
        f.write("".join(s) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
