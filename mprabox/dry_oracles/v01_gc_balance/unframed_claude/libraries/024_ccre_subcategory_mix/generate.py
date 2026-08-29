"""Experiment 024: Keep 30% high-GC cCRE (winner from 022), add cCRE subcategory diversity.

Mix:
- chr22, chr19, chr17, chr20: 3,000 each (12k, gene-dense base)
- whole_genome: 3,000
- cCRE PLS+DNase-H3K4me3 (high GC): 15,000 (30%, peak)
- cCRE dELS (distal enh, mid GC): 10,000
- cCRE pELS (proximal enh): 5,000
- cCRE CTCF-only: 5,000
Total: 50k

Adds 3 cCRE subcategories on top of 022's recipe.
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
rng = np.random.default_rng(240)


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
    ("PLS+DNase-H3K4me3", sample_ccre(lambda lbl: "PLS" in lbl or "DNase-H3K4me3" in lbl, 15000)),
    ("dELS", sample_ccre(lambda lbl: lbl.startswith("dELS"), 10000)),
    ("pELS", sample_ccre(lambda lbl: lbl.startswith("pELS"), 5000)),
    ("CTCF-only", sample_ccre(lambda lbl: lbl.startswith("CTCF-only"), 5000)),
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
