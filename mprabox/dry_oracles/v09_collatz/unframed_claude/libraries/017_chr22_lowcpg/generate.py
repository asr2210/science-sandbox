"""Experiment 017 — chr22 random tiles with CpG-island filter.

Drop CpG-island-like windows (high GC + high CpG obs/exp), keeping
the rest of the natural distribution. Hypothesis: removing only the
GC-rich CpG-island tail will improve HepG2 without hurting SKNSH
(which sits at 50% GC, far from the cut).

A "CpG island" is classically: GC>=50%, CpG obs/exp >= 0.6, len>=200bp.
We drop windows that meet ALL of: GC>=55% AND CpG_obs/exp>=0.6.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(17)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

def gc(s):
    return (s.count("G") + s.count("C")) / len(s)

def cpg_oe(s):
    cg = 0
    for i in range(len(s) - 1):
        if s[i] == "C" and s[i+1] == "G":
            cg += 1
    g = s.count("G"); c = s.count("C")
    if g == 0 or c == 0:
        return 0.0
    return cg * len(s) / (c * g)

out = Path(__file__).parent / "sequences_0.txt"
ok = 0; tries = 0; dropped_cpg = 0
gcs = []
with out.open("w") as f:
    while ok < N:
        tries += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        g = gc(s)
        if g >= 0.55 and cpg_oe(s) >= 0.6:
            dropped_cpg += 1
            continue
        f.write(s); f.write("\n")
        ok += 1
        if ok <= 5000:
            gcs.append(g)
print(f"Wrote {ok} sequences (tries {tries}, dropped_cpg {dropped_cpg}, accept {ok/tries:.2f})")
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f} min={min(gcs):.2f} max={max(gcs):.2f}")
