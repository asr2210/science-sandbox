"""
Experiment 004: 50/50 mix of random genomic windows + cCRE-centered windows.

Tests theory v3 (c): distributional breadth + motif density together
exceed either alone. Half the library is random genomic windows (broad
context, mostly non-regulatory) and half is cCRE-centered windows
(regulatory enrichment). Both halves come from hg38 primary chroms.

Predictions:
- eval_07/13 recover toward 0.55–0.60 (regulatory context restored)
- eval_04/09 hold near +0.50 (some cCRE benefit retained)
- eval_08 holds the partial recovery
- eval_01 lands around 0.54–0.57

Generalization argument: half the library teaches the model what real
*non-regulatory* genome looks like (background); the other half
teaches it what real *regulatory* elements look like. Both are needed
for a model that has to score sequences from any source (active in
seen cell types, active in unseen cell types, or non-functional).
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FA_PATH = os.path.join(ROOT, "data", "hg38.fa")
BED_PATH = os.path.join(ROOT, "data", "cCRE_v3_primary.bed")
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]

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

def sample_ccre(rng, fa, n):
    cres = []
    with open(BED_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            cres.append((parts[0], int(parts[1]), int(parts[2])))
    idx = rng.permutation(len(cres))
    chrom_len = {c: len(fa[c]) for c in {x[0] for x in cres}}
    seqs = []
    for i in idx:
        chrom, s, e = cres[int(i)]
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
        if len(seqs) == n:
            break
    return seqs

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)

    n_each = N // 2
    print(f"sampling {n_each} random genomic and {n_each} cCRE-centered")
    a = sample_random_genomic(rng, fa, n_each)
    b = sample_ccre(rng, fa, n_each)
    combined = a + b
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
