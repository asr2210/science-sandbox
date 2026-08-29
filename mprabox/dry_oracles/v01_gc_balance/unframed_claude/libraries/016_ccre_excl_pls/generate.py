"""Experiment 016: cCREs excluding PLS (promoter-like, which crashed alone).
Tests whether removing high-GC promoter elements lets the rest of cCREs do
better than the all-cCRE mix.
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

regions = []
with open(BED) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        chrom, start, end, _id1, _id2, label = parts[:6]
        if "PLS" in label:  # skip any PLS (with or without CTCF)
            continue
        regions.append((chrom, int(start), int(end)))
print(f"Got {len(regions)} non-PLS cCREs")

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

rng = np.random.default_rng(110)
idx = rng.choice(len(regions), size=N, replace=False)

seqs = []
for i in idx:
    chrom, start, end = regions[i]
    if chrom not in chrom_lens:
        continue
    center = (start + end) // 2
    p = max(0, min(center - L // 2, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)
# Top up
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
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {len(seqs)}")
