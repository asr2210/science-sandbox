"""
Experiment 006: 50/50 mix of random genomic + cell-type-balanced DHS index.

Tests theory v3 (d): cell-type-balanced regulatory sampling beats
cCRE (which is K562-biased) on HepG2/SK-N-SH generalization while
keeping K562 strength.

The DHS Index (Meuleman 2020) contains 3.6M consensus DNase peaks from
733 biosamples across 16 cell-type 'components' (Lymphoid, Cardiac,
Pulmonary, Stromal, Neural, etc.). The components are very unbalanced
(Primitive/embryonic has 627k, Stromal A has 56k). Uniform sampling
would replicate the K562 bias problem.

Design: sample equally across the 16 components — 1,562–1,563 from
each — for the regulatory half. Use the summit position from the DHS
index and extract a 200bp window centered there. The genomic half is
identical to exp 004 (25k uniform-by-length windows from primary
chroms).

Predictions vs exp 004 (mean=0.531, cCRE-based mix):
- HepG2 and SK-N-SH heads should improve (broader cell-type coverage)
- K562 should stay similar (still well-represented)
- eval_07/13 may improve further if the cell-type-balanced DHS has
  broader motif coverage than cCRE
- eval_01: predict 0.57–0.60

Generalization argument: the goal is a model that generalizes to
*unseen* cell types. A library sampled from 16 cell-type components
(rather than ENCODE's K562-dominant cCRE catalog) exposes the model
to regulatory grammar from many cell types, which should help it
predict regulatory activity in cell types we never label.
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
DHS_PATH = os.path.join(ROOT, "data", "dhs_index_primary.tsv")
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

def sample_dhs_balanced(rng, fa, n_total):
    # Bucket DHS by component
    buckets = defaultdict(list)
    with open(DHS_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            summit = int(parts[6])
            comp = parts[7]
            buckets[comp].append((chrom, summit))
    print("DHS buckets:", {k: len(v) for k, v in buckets.items()})

    comps = sorted(buckets.keys())
    n_each = n_total // len(comps)
    remainder = n_total - n_each * len(comps)
    chrom_len = {c: len(fa[c]) for c in CHROMS}

    seqs = []
    for ci, comp in enumerate(comps):
        # First few components get one extra to absorb the remainder
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
        print(f"  {comp}: {taken}")
    assert len(seqs) == n_total, len(seqs)
    return seqs

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    n_each = N // 2
    print(f"sampling {n_each} random genomic and {n_each} DHS (component-balanced)")
    a = sample_random_genomic(rng, fa, n_each)
    b = sample_dhs_balanced(rng, fa, n_each)
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
