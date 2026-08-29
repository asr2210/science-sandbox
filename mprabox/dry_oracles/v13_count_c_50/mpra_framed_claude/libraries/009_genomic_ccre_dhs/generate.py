"""
Experiment 009: 3-way mix — genomic + class-balanced cCRE + balanced DHS.

Tests the "complementary regulatory grammars" hypothesis from Cell 2025
iterative enhancer design paper: cCRE and DHS sequences carry
complementary information about regulatory grammar, and a model
trained on both does better than either alone.

Composition:
- 25,000 random genomic (50%)
- 12,500 class-balanced cCRE (2,500 per class, 5 classes)
- 12,500 component-balanced DHS (~782 per component, 16 components)
"""
import os
from collections import defaultdict
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FA_PATH = os.path.join(ROOT, "data", "hg38.fa")
BED_PATH = os.path.join(ROOT, "data", "cCRE_v3_primary.bed")
DHS_PATH = os.path.join(ROOT, "data", "dhs_index_primary.tsv")
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]

CLASS_FROM_LABEL = lambda label: label.split(",", 1)[0]
COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))

def sample_random_genomic(rng, fa, n):
    lengths = {c: len(fa[c]) for c in CHROMS}
    weights = np.array([lengths[c] for c in CHROMS], dtype=float)
    weights /= weights.sum()
    seqs = []
    while len(seqs) < n:
        chrom = CHROMS[rng.choice(len(CHROMS), p=weights)]
        start = rng.integers(0, lengths[chrom] - L)
        s = str(fa[chrom][start:start + L]).upper()
        if "N" in s:
            continue
        if rng.random() < 0.5:
            s = revcomp(s)
        seqs.append(s)
    return seqs

def sample_ccre_classbalanced(rng, fa, n_total):
    buckets = defaultdict(list)
    with open(BED_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            buckets[CLASS_FROM_LABEL(parts[4])].append((parts[0], int(parts[1]), int(parts[2])))
    classes = sorted(buckets.keys())
    n_each = n_total // len(classes)
    remainder = n_total - n_each * len(classes)
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    seqs = []
    for ci, cls in enumerate(classes):
        n_target = n_each + (1 if ci < remainder else 0)
        idx_perm = rng.permutation(len(buckets[cls]))
        taken = 0
        for i in idx_perm:
            chrom, s, e = buckets[cls][int(i)]
            mid = (s + e) // 2
            ws, we = mid - L // 2, mid - L // 2 + L
            if ws < 0 or we > chrom_len[chrom]:
                continue
            seq = str(fa[chrom][ws:we]).upper()
            if "N" in seq:
                continue
            if rng.random() < 0.5:
                seq = revcomp(seq)
            seqs.append(seq)
            taken += 1
            if taken == n_target:
                break
    return seqs

def sample_dhs_balanced(rng, fa, n_total):
    buckets = defaultdict(list)
    with open(DHS_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            buckets[parts[7]].append((parts[0], int(parts[6])))
    comps = sorted(buckets.keys())
    n_each = n_total // len(comps)
    remainder = n_total - n_each * len(comps)
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    seqs = []
    for ci, comp in enumerate(comps):
        n_target = n_each + (1 if ci < remainder else 0)
        idx_perm = rng.permutation(len(buckets[comp]))
        taken = 0
        for i in idx_perm:
            chrom, summit = buckets[comp][int(i)]
            ws = summit - L // 2
            we = ws + L
            if ws < 0 or we > chrom_len[chrom]:
                continue
            s = str(fa[chrom][ws:we]).upper()
            if "N" in s:
                continue
            if rng.random() < 0.5:
                s = revcomp(s)
            seqs.append(s)
            taken += 1
            if taken == n_target:
                break
    return seqs

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    n_gen, n_ccre, n_dhs = 25000, 12500, 12500
    a = sample_random_genomic(rng, fa, n_gen)
    print(f"genomic: {len(a)}")
    b = sample_ccre_classbalanced(rng, fa, n_ccre)
    print(f"cCRE: {len(b)}")
    c = sample_dhs_balanced(rng, fa, n_dhs)
    print(f"DHS: {len(c)}")
    combined = a + b + c
    rng.shuffle(combined)
    with open(OUT, "w") as f:
        f.write("\n".join(combined) + "\n")
    with open(OUT) as f:
        lines = f.read().splitlines()
    assert len(lines) == N
    for l in lines[:5]:
        assert len(l) == L and set(l) <= set("ACGT")
    print(f"wrote {len(lines)} sequences")

if __name__ == "__main__":
    main()
