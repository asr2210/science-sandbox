"""Experiment 003: Stratified sample of ENCODE V4 cCREs by class.

Source: ENCFF420VPZ.bed (2.35M elements with proper classifications).
50k sequences, stratified across regulatory categories:
- PLS  (promoter-like, 47.5k available) -> 10k
- pELS (proximal enhancer, 249k)        -> 10k
- dELS (distal enhancer, 1.47M)         -> 15k
- TF   (TF-binding, 105k)               -> 5k
- CA-* (chromatin accessible, 477k)     -> 10k
Total = 50,000

Rationale: balanced exposure to all regulatory grammar classes, not
just the dominant dELS class. PLS sequences carry promoter motifs
(TATA, INR, GC) that differ from enhancer grammar. The model should
learn each class.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BED = os.path.join(ROOT, "data", "ENCFF420VPZ.bed")
FA = os.path.join(ROOT, "data", "hg38.fa")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

TARGETS = {"PLS": 10_000, "pELS": 10_000, "dELS": 15_000, "TF": 5_000}
CA_TARGET = 10_000  # any CA-* class

rng = np.random.default_rng(SEED)

# Load BED grouped by class
by_class = {}
with open(BED) as f:
    for line in f:
        cols = line.rstrip().split("\t")
        chrom, start, end, cls = cols[0], int(cols[1]), int(cols[2]), cols[9]
        if "_" in chrom or chrom == "chrM":
            continue
        key = cls if cls in TARGETS else ("CA" if cls.startswith("CA") else None)
        if key is None:
            continue
        by_class.setdefault(key, []).append((chrom, start, end))

print("Class sizes:", {k: len(v) for k, v in by_class.items()})

fa = Fasta(FA, sequence_always_upper=True)

def extract(regions, target, key):
    n_take = min(target, len(regions))
    # Sample more than needed for rejection
    indices = rng.choice(len(regions), size=min(int(n_take * 1.3), len(regions)), replace=False)
    out = []
    for i in indices:
        chrom, start, end = regions[i]
        center = (start + end) // 2
        s = center - L // 2
        e = s + L
        if s < 0 or e > len(fa[chrom]):
            continue
        seq = str(fa[chrom][s:e])
        if "N" in seq or len(seq) != L:
            continue
        out.append(seq)
        if len(out) == target:
            break
    print(f"  {key}: got {len(out)}/{target}")
    return out

all_seqs = []
for cls, target in TARGETS.items():
    all_seqs.extend(extract(by_class[cls], target, cls))
all_seqs.extend(extract(by_class["CA"], CA_TARGET, "CA"))

# Top up if any class came short
while len(all_seqs) < 50_000:
    # backfill from dELS (largest pool)
    extra = extract(by_class["dELS"], 50_000 - len(all_seqs) + 100, "dELS_topup")
    for s in extra:
        if s not in all_seqs:
            all_seqs.append(s)
            if len(all_seqs) >= 50_000:
                break

all_seqs = all_seqs[:50_000]
assert len(all_seqs) == 50_000

# Shuffle so classes don't appear in blocks
rng.shuffle(all_seqs)

with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")

print(f"wrote {len(all_seqs)} sequences to {OUT}")
