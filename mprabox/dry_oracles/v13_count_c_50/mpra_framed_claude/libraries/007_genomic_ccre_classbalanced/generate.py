"""
Experiment 007: 50/50 mix of random genomic + class-balanced cCRE.

Tests theory v4: compositional diversity within the regulatory half
matters more than cell-type balance. The cCRE catalog has 5 distinct
element classes with different sequence regimes:
  - PLS (promoter-like)        ~35k    high-GC, CpG island enriched
  - pELS (proximal enhancer)   ~142k
  - dELS (distal enhancer)     ~668k   dominates uniform sample (72%)
  - CTCF-only                  ~57k    CTCF motif enriched
  - DNase-H3K4me3              ~26k

Exp 004 (uniform cCRE) is 72% dELS. Exp 007 forces 5,000 per class
= 25,000 cCRE total, half the library, paired with 25,000 random
genomic.

Predictions vs exp 004:
- eval_04/09 (composition-axis): 0.52 → 0.55+ (promoter and CTCF
  classes add GC/CpG diversity)
- eval_07/13: similar (~0.62)
- eval_01: 0.57 → 0.58–0.60
- Mean: 0.53 → 0.54

Generalization argument: a model trained on diverse cCRE classes sees
ALL the major regulatory element types — promoters, distal enhancers,
proximal enhancers, CTCF anchors, generic open chromatin. This
breadth of regulatory element types prepares it for any unseen cell
type, whose regulatory landscape is also composed of these same
classes.
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
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]

# We treat each composite label as its own class - 9 classes - but the user-facing
# 'class' is the primary part before the comma. We bucket by primary class.
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
            chrom = parts[0]
            start, end = int(parts[1]), int(parts[2])
            label = parts[4]
            cls = CLASS_FROM_LABEL(label)
            buckets[cls].append((chrom, start, end))
    print("classes:", {k: len(v) for k, v in buckets.items()})
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
        print(f"  {cls}: {taken}")
    assert len(seqs) == n_total, len(seqs)
    return seqs

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    n_each = N // 2
    print(f"sampling {n_each} random genomic and {n_each} class-balanced cCRE")
    a = sample_random_genomic(rng, fa, n_each)
    b = sample_ccre_classbalanced(rng, fa, n_each)
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
