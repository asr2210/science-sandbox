"""Experiment 020: 7-source extreme-variance real DNA mix.
Builds on 019 (0.6895) by adding the GC extremes more aggressively:
- chr22 random (gene-dense, ~48% GC)
- chr19 random (gene-dense, higher GC)
- whole genome random (background, ~41%)
- chrX random (mid-GC)
- chrY random (repeat/heterochromatin, AT-rich)
- K562 chromHMM Het+Quies (very AT-rich)
- cCRE PLS only (very GC-rich CpG islands)
~7,200 each, total 50k. Tests whether more extreme variance pushes past 0.6895.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
BED = os.path.join(ROOT, "GRCh38-cCREs.bed")
CHROMHMM = os.path.join(ROOT, "E123_K562_chromHMM.bed")
L = 200
PER = 7200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}
rng = np.random.default_rng(200)


def sample_chr_random(chrom, n):
    out, attempts = [], 0
    cl = chrom_lens[chrom]
    while len(out) < n and attempts < n * 20:
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


def sample_bed(bed_path, n, filter_fn=None, col=3):
    regions = []
    with open(bed_path) as f:
        for line in f:
            if line.startswith("track"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < max(3, col + 1):
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            label = parts[col] if col < len(parts) else ""
            if filter_fn is None or filter_fn(label):
                regions.append((chrom, start, end))
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


def sample_ccre(filter_fn, n):
    return sample_bed(BED, n, filter_fn=filter_fn, col=5)


s1 = sample_chr_random("chr22", PER)
print(f"chr22: {len(s1)}")
s2 = sample_chr_random("chr19", PER)
print(f"chr19: {len(s2)}")
s3 = sample_whole_genome(PER)
print(f"whole_genome: {len(s3)}")
s4 = sample_chr_random("chrX", PER)
print(f"chrX: {len(s4)}")
s5 = sample_chr_random("chrY", PER)
print(f"chrY: {len(s5)}")
s6 = sample_bed(CHROMHMM, PER, filter_fn=lambda lbl: lbl in ("9_Het", "15_Quies"), col=3)
print(f"chromHMM Het+Quies: {len(s6)}")
s7 = sample_ccre(lambda lbl: "PLS" in lbl, PER)
print(f"cCRE PLS: {len(s7)}")

seqs = s1 + s2 + s3 + s4 + s5 + s6 + s7
print(f"Total: {len(seqs)}")
rng.shuffle(seqs)
seqs = seqs[:50_000]
print(f"Writing {len(seqs)}")
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

# Print GC distribution
gcs = [(s.count("G") + s.count("C")) / L for s in seqs]
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f} min={min(gcs):.3f} max={max(gcs):.3f}")
