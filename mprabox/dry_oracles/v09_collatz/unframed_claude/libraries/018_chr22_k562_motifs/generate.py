"""Experiment 018 — chr22 tiles + erythroid motifs to boost K562.

K562 is the laggard: ~0.14 regardless of recipe. Erythroid TFs:
GATA1 (AGATAA, 6bp), KLF1 (CACACC, 6bp). Insert 1 of each per seq
at random positions (overwriting 12bp out of 200 — 6% displacement,
less than exp 011's 15%).

Goal: K562 +0.01-0.02 with minimal HepG2/SKNSH cost.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(18)
N, L = 50_000, 200

# Erythroid motifs — strand-balanced
GATA = ["AGATAA", "TTATCT"]  # GATA1 fwd + rev-comp
KLF  = ["CACACC", "GGTGTG"]  # KLF1 fwd + rev-comp

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

def implant(s, motif, rng):
    pos = int(rng.integers(20, L - 20 - len(motif)))
    return s[:pos] + motif + s[pos + len(motif):]

out = Path(__file__).parent / "sequences_0.txt"
ok = 0
with out.open("w") as f:
    while ok < N:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        g = GATA[int(rng.integers(0, 2))]
        k = KLF[int(rng.integers(0, 2))]
        s = implant(s, g, rng)
        s = implant(s, k, rng)
        assert len(s) == L
        f.write(s); f.write("\n")
        ok += 1
print(f"Wrote {ok} to {out}")
