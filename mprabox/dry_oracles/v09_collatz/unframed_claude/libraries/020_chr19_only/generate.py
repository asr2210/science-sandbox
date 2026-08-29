"""Experiment 020 — chr19 only (48% GC, the highest-GC chromosome we have).

chr22 (47% GC) gave us 0.3202; chr18 (40% GC) gave 0.3043. The trend
suggests slightly higher GC could be better since SKNSH peaks at 50%.
chr19 is the closest to 50% — should be neutral or better.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(20)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr19.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr19: {len(seq):,}")

out = Path(__file__).parent / "sequences_0.txt"
ok = 0
gcs = []
with out.open("w") as f:
    while ok < N:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        f.write(s); f.write("\n")
        ok += 1
        if ok <= 5000:
            gcs.append((s.count("G") + s.count("C")) / L)
print(f"Wrote {ok}; GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
