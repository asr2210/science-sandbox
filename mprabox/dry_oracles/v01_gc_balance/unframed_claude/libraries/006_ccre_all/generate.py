"""Experiment 006: 50k 200bp sequences from ENCODE cCREs (all categories).
Sample cCREs uniformly, take 200bp window centered on each.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
BED = os.path.join(ROOT, "GRCh38-cCREs.bed")
N = 50_000
L = 200

print("Loading bed...")
regions = []
with open(BED) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        regions.append((chrom, start, end))
print(f"Loaded {len(regions)} cCREs")

print("Loading fasta...")
fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

rng = np.random.default_rng(47)
idx = rng.choice(len(regions), size=N, replace=False)

seqs = []
for i in idx:
    chrom, start, end = regions[i]
    if chrom not in chrom_lens:
        continue
    center = (start + end) // 2
    p = center - L // 2
    p = max(0, min(p, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) != L or "N" in s:
        continue
    seqs.append(s)
print(f"Got {len(seqs)} sequences")

# Top up with extra cCREs if some had Ns
extra_iter = iter(rng.permutation(len(regions)))
while len(seqs) < N:
    i = next(extra_iter)
    chrom, start, end = regions[i]
    if chrom not in chrom_lens:
        continue
    center = (start + end) // 2
    p = max(0, min(center - L // 2, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)

seqs = seqs[:N]
assert len(seqs) == N
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences")
