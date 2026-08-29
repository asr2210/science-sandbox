"""Experiment 023: push cCRE PLS+DNase-H3K4me3 to 50% of library to test trend.

Mix:
- chr22, chr19, chr17, chr20, whole_genome: 3,000 each (15k)
- cCRE all: 10,000
- cCRE PLS+DNase-H3K4me3: 25,000 (50%)
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
rng = np.random.default_rng(230)


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


def sample_whole_genome(n):
    chroms = [f"chr{i}" for i in range(1, 23)] + ["chrX"]
    cl = {c: chrom_lens[c] for c in chroms}
    total = sum(cl.values())
    weights = np.array([cl[c] for c in chroms]) / total
    out, attempts = [], 0
    while len(out) < n and attempts < n * 5:
        attempts += 1
        c = rng.choice(chroms, p=weights)
        p = rng.integers(0, cl[c] - L)
        s = str(fa[c][p:p+L])
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
    # if not enough, sample with replacement
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
    ("chr22", sample_chr_random("chr22", 3000)),
    ("chr19", sample_chr_random("chr19", 3000)),
    ("chr17", sample_chr_random("chr17", 3000)),
    ("chr20", sample_chr_random("chr20", 3000)),
    ("whole_genome", sample_whole_genome(3000)),
    ("cCRE_all", sample_ccre(None, 10000)),
    ("cCRE_high_GC", sample_ccre(lambda lbl: "PLS" in lbl or "DNase-H3K4me3" in lbl, 25000)),
]
for name, s in sources:
    print(f"{name}: {len(s)}")
seqs = sum((s for _, s in sources), [])
print(f"Total: {len(seqs)}")
rng.shuffle(seqs)
seqs = seqs[:50_000]
print(f"Final: {len(seqs)}")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

gcs = [(s.count("G") + s.count("C")) / L for s in seqs]
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
