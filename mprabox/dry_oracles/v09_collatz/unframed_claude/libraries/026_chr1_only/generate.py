"""Experiment 026 — chr1 only random tiles.

chr1 (42% GC) is the largest chromosome (249Mb) and untested alone.
Provides another data point on the chr-GC curve:
  chr18 (40%): 0.3043
  chr1  (42%): ?
  chr22 (47%): 0.3202
  chr19 (48%): 0.3198
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(26)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr1.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr1: {len(seq):,}")

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
