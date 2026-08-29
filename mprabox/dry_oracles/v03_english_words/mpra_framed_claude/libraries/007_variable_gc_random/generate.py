"""
007 — Variable-GC random library.

Each sequence's GC content is sampled uniformly from [0.25, 0.75].
Diagnostic: does broadening the compositional distribution beyond uniform-50%-GC
hurt or help K562/HepG2 r?
"""
import numpy as np
from pathlib import Path

L = 200
N = 50_000
SEED = 7
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
alphabet_gc = np.array(list("GC"))
alphabet_at = np.array(list("AT"))

seqs = []
for _ in range(N):
    gc_frac = rng.uniform(0.25, 0.75)
    # Per-position Bernoulli choice between GC and AT, then pick a base.
    is_gc = rng.random(L) < gc_frac
    bases = np.where(
        is_gc,
        alphabet_gc[rng.integers(0, 2, size=L)],
        alphabet_at[rng.integers(0, 2, size=L)],
    )
    seqs.append("".join(bases.tolist()))

with OUT.open("w") as f:
    for s in seqs:
        f.write(s)
        f.write("\n")
print(f"wrote {N} x {L}bp variable-GC random sequences to {OUT}")
print(f"GC range: 25-75%")
