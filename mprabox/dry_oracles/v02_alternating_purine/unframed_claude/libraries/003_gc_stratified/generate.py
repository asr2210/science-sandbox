"""003 — GC-stratified library.

Each sequence has a GC content sampled uniformly from [0.2, 0.8].
Tests hypothesis that the scorer rewards library DIVERSITY along a major
sequence feature (GC content), particularly for SKNSH.

Hypothesis: if mean_r rises (especially SKNSH), variance in GC content drives
SKNSH baseline. If mean_r stays similar, GC isn't the lever.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(3)
N, L = 50_000, 200
ALPH_GC = np.array(list("GC"))
ALPH_AT = np.array(list("AT"))

gcs = rng.uniform(0.2, 0.8, size=N)
lines = []
for gc in gcs:
    n_gc = rng.binomial(L, gc)
    pos = rng.permutation(L)
    seq = np.empty(L, dtype="<U1")
    seq[pos[:n_gc]] = ALPH_GC[rng.integers(0, 2, size=n_gc)]
    seq[pos[n_gc:]] = ALPH_AT[rng.integers(0, 2, size=L - n_gc)]
    lines.append("".join(seq))

out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {N} sequences to {out}")
