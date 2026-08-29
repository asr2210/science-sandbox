"""Experiment 008: PLS (promoter-like signature) cCREs.
~40k PLS (with and without CTCF). For 50k, sample with replacement or
take multiple 200bp windows from longer PLS regions.
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
        if "PLS" in label:  # any PLS, with or without CTCF
            regions.append((chrom, int(start), int(end)))
print(f"Got {len(regions)} PLS regions")

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

rng = np.random.default_rng(49)
seqs = []
# Sample with replacement; jitter the window center within the region for diversity
while len(seqs) < N:
    i = rng.integers(0, len(regions))
    chrom, start, end = regions[i]
    if chrom not in chrom_lens:
        continue
    width = end - start
    # Random center inside the region (with at least L/2 buffer)
    if width < L:
        # Use the center of the region; just expand
        center = (start + end) // 2
    else:
        offset = rng.integers(0, width)
        center = start + offset
    p = max(0, min(center - L // 2, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)
print(f"Got {len(seqs)} sequences")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print("Done.")
