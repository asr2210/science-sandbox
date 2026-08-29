"""
Experiment 005: 3-way mix — random uniform + random genomic + cCRE-centered.

Goal: maximize distributional breadth. Tests whether including
*explicitly non-genomic* sequences (uniform random) recovers eval_08
without giving up wins elsewhere.

Composition: ~16,667 each (50,000 / 3, with rounding). Shuffled.

Predictions:
- eval_08 → 0.20–0.35 (recovery toward exp 001's 0.58)
- eval_07/13 → 0.60+
- eval_01 → 0.54–0.57

Generalization argument: a model that has seen uniformly-random as
well as natural sequences during training cannot assume "all sequences
look like the human genome." For unseen cell types, regulatory
elements may have unusual compositional bias or include
non-canonical context. Training on a mixture that spans genomic and
non-genomic compositional regimes prepares the model to handle test
sequences from any distribution.
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

def sample_uniform(rng, n):
    alphabet = np.array(list("ACGT"))
    idx = rng.integers(0, 4, size=(n, L), dtype=np.int8)
    return ["".join(row) for row in alphabet[idx]]

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

    # 16668 + 16666 + 16666 = 50000
    n_uni = 16668
    n_gen = 16666
    n_cre = 16666
    print(f"sampling {n_uni} uniform, {n_gen} genomic, {n_cre} cCRE")

    a = sample_uniform(rng, n_uni)
    b = sample_random_genomic(rng, fa, n_gen)
    c = sample_ccre(rng, fa, n_cre)
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
