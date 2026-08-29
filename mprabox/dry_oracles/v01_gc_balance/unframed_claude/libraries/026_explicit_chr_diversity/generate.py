"""Experiment 026: 022 recipe + replace whole_genome with explicit chr diversity.
Add chr1, chr11, chr16 (mid-density chromosomes) for variance without length bias.

Mix:
- chr22, chr19, chr17, chr20: 4,000 each = 16k
- chr1, chr11, chr16: ~1,333 each = 4k (replaces whole_genome, gene-dense biased)
- cCRE_all: 15,000
- cCRE PLS+DNase-H3K4me3: 15,000
Total: 50k
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
BED = os.path.join(ROOT, "GRCh38-cCREs.bed")
L = 200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}
rng = np.random.default_rng(260)


def sample_chr_random(chrom, n):
    out, attempts = [], 0
    cl = chrom_lens[chrom]
    while len(out) < n and attempts < n * 10:
        attempts += 1
        p = rng.integers(0, cl - L)
        s = str(fa[chrom][p:p+L])
        if len(s) == L and "N" not in s:
            out.append(s)
    return out


def sample_ccre(filter_fn, n):
    regions = []
    with open(BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            label = parts[5]
            if filter_fn is None or filter_fn(label):
                regions.append((chrom, start, end))
    if len(regions) < n:
        idx = rng.integers(0, len(regions), size=n)
    else:
        idx = rng.permutation(len(regions))
    out = []
    for i in idx:
        if len(out) >= n:
            break
        chrom, start, end = regions[i]
        if chrom not in chrom_lens:
            continue
        center = (start + end) // 2
        p = max(0, min(center - L // 2, chrom_lens[chrom] - L))
        s = str(fa[chrom][p:p+L])
        if len(s) == L and "N" not in s:
            out.append(s)
    return out


sources = [
    ("chr22", sample_chr_random("chr22", 4000)),
    ("chr19", sample_chr_random("chr19", 4000)),
    ("chr17", sample_chr_random("chr17", 4000)),
    ("chr20", sample_chr_random("chr20", 4000)),
    ("chr1",  sample_chr_random("chr1",  1333)),
    ("chr11", sample_chr_random("chr11", 1333)),
    ("chr16", sample_chr_random("chr16", 1334)),
    ("cCRE_all", sample_ccre(None, 15000)),
    ("cCRE_high_GC", sample_ccre(lambda lbl: "PLS" in lbl or "DNase-H3K4me3" in lbl, 15000)),
]
for name, s in sources:
    print(f"{name}: {len(s)}")
seqs = sum((s for _, s in sources), [])
print(f"Total: {len(seqs)}")
rng.shuffle(seqs)
seqs = seqs[:50_000]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

gcs = [(s.count("G") + s.count("C")) / L for s in seqs]
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
