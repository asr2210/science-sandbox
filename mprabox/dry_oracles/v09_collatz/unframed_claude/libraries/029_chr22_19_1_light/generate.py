"""Experiment 029 — chr22 + chr19 + chr1 light dose (47.5/47.5/5).

Exp 027 (chr22+chr19 50/50) = 0.3215 best ever.
Exp 028 (40/40/20 with chr1) = 0.3197 — chr1 at 20% hurt SKNSH.
Test: does a 5% chr1 dose hit a sweet spot? If marginal cost of chr1
on SKNSH is roughly linear, 5% should be ~-0.0004 vs 27.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(29)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
chrom_seq = {}
for name in ("chr22", "chr19", "chr1"):
    parts = []
    with (ROOT / "data" / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"): continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)

def sample(name, k):
    seq = chrom_seq[name]
    out = []
    while len(out) < k:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        out.append(s)
    return out

n1 = int(0.05 * N)  # 2500
n22 = (N - n1) // 2  # 23750
n19 = N - n22 - n1  # 23750

all_seqs = sample("chr22", n22) + sample("chr19", n19) + sample("chr1", n1)
rng.shuffle(all_seqs)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for s in all_seqs:
        f.write(s); f.write("\n")
print(f"Wrote {len(all_seqs)} (chr22={n22}, chr19={n19}, chr1={n1})")
