"""Experiment 019: Maximum-variance real DNA library.
Mix multiple real-DNA sources to maximize per-sequence GC variance:
- 10k chr22 random (gene-dense)
- 10k whole-genome random (background)
- 10k cCRE all (regulatory)
- 10k high-GC cCREs (PLS/CpG islands, capped to avoid extreme)
- 10k low-GC chr X / intergenic regions (heterochromatin-like)

Tests whether maximizing biologically-meaningful variance pushes past 0.684.
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
rng = np.random.default_rng(140)

def sample_chr_random(chrom, n):
    out = []
    cl = chrom_lens[chrom]
    attempts = 0
    while len(out) < n and attempts < n * 5:
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
    out = []
    attempts = 0
    while len(out) < n and attempts < n * 5:
        attempts += 1
        c = rng.choice(chroms, p=weights)
        p = rng.integers(0, cl[c] - L)
        s = str(fa[c][p:p+L])
        if len(s) == L and "N" not in s:
            out.append(s)
    return out

def sample_ccre(filter_fn=None, n=10_000):
    regions = []
    with open(BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            chrom, start, end, _id1, _id2, label = parts[:6]
            if filter_fn is None or filter_fn(label):
                regions.append((chrom, int(start), int(end)))
    order = rng.permutation(len(regions))
    out = []
    for i in order:
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

s1 = sample_chr_random("chr22", 10_000)
print(f"chr22 random: {len(s1)}")
s2 = sample_whole_genome(10_000)
print(f"whole genome: {len(s2)}")
s3 = sample_ccre(filter_fn=None, n=10_000)
print(f"cCRE all: {len(s3)}")
s4 = sample_ccre(filter_fn=lambda label: "PLS" in label or "DNase-H3K4me3" in label, n=10_000)
print(f"cCRE PLS+DNase-H3K4me3 (high GC): {len(s4)}")
# Low-GC: use chr X random which is more AT-rich
s5 = sample_chr_random("chrX", 10_000)
print(f"chrX random: {len(s5)}")

seqs = s1 + s2 + s3 + s4 + s5
print(f"Total: {len(seqs)}")
rng.shuffle(seqs)
seqs = seqs[:50_000]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print("Wrote.")
