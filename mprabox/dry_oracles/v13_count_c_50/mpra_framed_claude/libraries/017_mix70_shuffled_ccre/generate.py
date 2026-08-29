"""Experiment 017: motif-vs-composition probe.

Same recipe as 013 (35k mc5 genomic + 15k type-balanced cCREs from chr5
set) but the 15k cCRE supplement is REPLACED with their dinucleotide
shuffles. Composition (GC, dinuc freqs) preserved per-sequence; motif
identity destroyed.

If 017 ≈ 013 → cCRE value is compositional.
If 017 << 013 → cCRE value is motif-grammatical.
If 017 between 004 (no supplement) and 013 → both contribute.
"""
from pathlib import Path
import sys
import numpy as np
from pyfaidx import Fasta

# import dinuc_shuffle from exp 006
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006_dinuc_shuffled_multichrom"))
from generate import dinuc_shuffle  # noqa: E402

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_CCRE = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")

per_chrom = N_GENOMIC // len(CHROMS)
genomic = []
for c in CHROMS:
    chrom_len = len(fas[c][c])
    collected = []
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L, size=4 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

# cCREs grouped by primary type
chrom_set = set(CHROMS)
ccres_by_type = {"PLS": [], "pELS": [], "dELS": [],
                 "CTCF-only": [], "DNase-H3K4me3": []}
with BED.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] not in chrom_set:
            continue
        primary = parts[5].split(",")[0]
        if primary in ccres_by_type:
            mid = (int(parts[1]) + int(parts[2])) // 2
            ccres_by_type[primary].append((parts[0], mid))

per_type = N_CCRE // 5
ccre_seqs = []
for t in ccres_by_type:
    pool = ccres_by_type[t]
    idx = rng.choice(len(pool), size=min(len(pool), 4 * per_type), replace=False)
    type_seqs = []
    for i in idx:
        if len(type_seqs) >= per_type:
            break
        chrom, mid = pool[i]
        start, end = mid - HALF, mid - HALF + L
        if start < 0 or end > len(fas[chrom][chrom]):
            continue
        s = fas[chrom][chrom][start:end]
        if len(s) == L and set(s).issubset(valid):
            type_seqs.append(s)
    ccre_seqs.extend(type_seqs)
assert len(ccre_seqs) == N_CCRE

# Shuffle cCREs to destroy motif identity, preserve composition
shuffled_ccres = [dinuc_shuffle(s, rng) for s in ccre_seqs]

# Sanity check
from collections import Counter
def dincount(s):
    return Counter(s[i:i+2] for i in range(len(s)-1))
matches = sum(1 for a, b in zip(ccre_seqs[:200], shuffled_ccres[:200])
              if dincount(a) == dincount(b))
print(f"cCRE dinuc preservation: {matches}/200")

all_seqs = genomic + shuffled_ccres
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 15k DINUC-SHUFFLED cCREs (motif removed).")
