"""
Experiment 014: 4-way — 10% uniform random ACGT dose.

Exp 013 (5% uniform) was NEW BEST (mean=0.546). Test if 10% lifts
further. Dose-response: 33% (exp 005) pollutes, 5% (exp 013) is a free
win. Find the peak.

Composition:
- 20,000 random genomic (40%)
- 20,000 class-balanced cCRE (4,000/class, 40%)
- 5,000 CpG islands (10%)
- 5,000 uniform random ACGT (10%)
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
CPG_PATH = os.path.join(ROOT, "data", "cpg_islands.bed")
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
PRIM = set(CHROMS)

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

def sample_cpgi(rng, fa, n_total):
    elems = []
    with open(CPG_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in PRIM:
                continue
            elems.append((chrom, int(parts[1]), int(parts[2])))
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    idx_perm = rng.permutation(len(elems))
    seqs = []
    for i in idx_perm:
        chrom, s, e = elems[int(i)]
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
        if len(seqs) == n_total:
            break
    return seqs

def sample_uniform_random(rng, n):
    bases = np.array(list("ACGT"))
    arr = rng.integers(0, 4, size=(n, L))
    return ["".join(bases[row]) for row in arr]

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    n_gen, n_ccre, n_cpgi, n_uni = 20000, 20000, 5000, 5000
    a = sample_random_genomic(rng, fa, n_gen); print(f"genomic: {len(a)}")
    b = sample_ccre_classbalanced(rng, fa, n_ccre); print(f"cCRE: {len(b)}")
    c = sample_cpgi(rng, fa, n_cpgi); print(f"CpGi: {len(c)}")
    d = sample_uniform_random(rng, n_uni); print(f"uniform: {len(d)}")
    combined = a + b + c + d
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
