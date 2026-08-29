"""Experiment 015 — multi-chromosome real DNA tiles.

Theory v6 says real DNA wins; theory v7 says library GC diversity helps.
chr22 alone gave 0.3202; chr18 alone 0.3043. Mix chr1/18/19/22 in equal
parts to broaden the GC distribution while keeping natural composition.

If multi-chrom > chr22 alone: diversity helps.
If multi-chrom < chr22 alone: chr22 has something special (or chr18's
AT-richness drags SKNSH down too far in the mix).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(15)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
chroms = ("chr1", "chr18", "chr19", "chr22")
chrom_seq = {}
for name in chroms:
    parts = []
    with (ROOT / "data" / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"): continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)
    print(f"{name}: {len(chrom_seq[name]):,}")

per_chrom = N // len(chroms)  # 12,500 each
out = Path(__file__).parent / "sequences_0.txt"

def sample(seq, k, rng):
    seqs = []
    while len(seqs) < k:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        seqs.append(s)
    return seqs

all_seqs = []
for name in chroms:
    all_seqs.extend(sample(chrom_seq[name], per_chrom, rng))

# top up if rounding short
while len(all_seqs) < N:
    all_seqs.extend(sample(chrom_seq["chr22"], N - len(all_seqs), rng))

rng.shuffle(all_seqs)
all_seqs = all_seqs[:N]

with out.open("w") as f:
    for s in all_seqs:
        f.write(s); f.write("\n")
print(f"Wrote {len(all_seqs)} to {out}")
