"""Experiment 024 — chr22 + single NF-Y (CCAAT) motif at center.

NF-Y/CCAAT is a universal activator (active in K562, HepG2, SKNSH).
Only 5bp. Place at position 95 (center). Minimal displacement (2.5%).
Test if even ONE motif beats real DNA alone or if zero-motif is best.

Vs exp 011 (3 motifs, 0.3152 = drop) and 018 (2 motifs, 0.3174 = drop):
1 motif might be the sweet spot.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(24)
N, L = 50_000, 200
MOTIFS = ["CCAAT", "ATTGG"]  # NF-Y forward + reverse comp
CENTER = (L - 5) // 2  # position 97 for 200bp

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

out = Path(__file__).parent / "sequences_0.txt"
ok = 0
with out.open("w") as f:
    while ok < N:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        m = MOTIFS[int(rng.integers(0, 2))]
        s2 = s[:CENTER] + m + s[CENTER + len(m):]
        assert len(s2) == L
        f.write(s2); f.write("\n")
        ok += 1
print(f"Wrote {ok} to {out}")
