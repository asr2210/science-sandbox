"""Experiment 009 — Real human DNA tiles.

Sample 50,000 random 200bp windows from human chr22 (hg38, downloaded
to data/chr22.fa). Skip windows containing N or runs of low complexity.

If real DNA scores much higher than random, the model is calibrated
to natural sequence statistics. If similar, we know motifs aren't
the bottleneck.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(9)
N, L = 50_000, 200

# Load sequence (concat all non-header lines)
fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
lines = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"):
            continue
        lines.append(line.strip().upper())
seq = "".join(lines)
print(f"chr22 length: {len(seq):,}")

# Sample random windows that contain only ACGT
out = Path(__file__).parent / "sequences_0.txt"
ok = 0
attempts = 0
with out.open("w") as f:
    while ok < N:
        attempts += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s:
            continue
        # avoid very low-complexity runs (>= 20bp same base)
        if any(s.count(c * 20) > 0 for c in "ACGT"):
            continue
        f.write(s); f.write("\n")
        ok += 1
print(f"Wrote {N} sequences (attempted {attempts}) to {out}")
