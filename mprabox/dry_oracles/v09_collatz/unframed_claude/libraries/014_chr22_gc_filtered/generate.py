"""Experiment 014 — chr22 windows filtered to 45-50% GC.

Real chr22 random tiles (best so far at 0.3202) but filtered to the
"sweet GC band" — drop the very GC-rich windows (CpG islands) and the
very AT-rich ones (heterochromatin). Hypothesis: a tighter,
HepG2-friendly composition without losing SKNSH (50% GC peak).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(14)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"):
            continue
        parts.append(line.strip().upper())
seq = "".join(parts)

out = Path(__file__).parent / "sequences_0.txt"
ok = 0; tries = 0
with out.open("w") as f:
    while ok < N:
        tries += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s or any(s.count(c * 20) > 0 for c in "ACGT"):
            continue
        gc = (s.count("G") + s.count("C")) / L
        if gc < 0.45 or gc > 0.50:
            continue
        f.write(s); f.write("\n")
        ok += 1
print(f"Wrote {ok} sequences (tries {tries}, accept rate {ok/tries:.2f}) to {out}")
