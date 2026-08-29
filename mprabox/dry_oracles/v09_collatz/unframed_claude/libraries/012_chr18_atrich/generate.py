"""Experiment 012 — Real DNA from chr18 (AT-rich, ~40% GC).

chr18 is gene-poor and AT-biased. If HepG2 model rewards AT-rich
natural DNA even more than chr22 (47% GC) gave us, chr18 should push
HepG2 higher. Risk: SKNSH may drop slightly off its 50% GC peak.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(12)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr18.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"):
            continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr18 length: {len(seq):,}")

out = Path(__file__).parent / "sequences_0.txt"
ok = 0; tries = 0
with out.open("w") as f:
    while ok < N:
        tries += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s:
            continue
        if any(s.count(c * 20) > 0 for c in "ACGT"):
            continue
        f.write(s); f.write("\n")
        ok += 1
print(f"Wrote {ok} sequences (tries {tries}) to {out}")
