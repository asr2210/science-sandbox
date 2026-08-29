"""Experiment 020: composite supplement — shuffled-cCRE + GC-filter.

35k mc5 + 7.5k dinucleotide-shuffled type-balanced cCREs (broad
composition, motif-free) + 7.5k random mc5 windows filtered to
GC ∈ [0.50, 0.80] (concentrated high-GC tail).

Tests whether the two compositional axes (broad multimodal vs narrow
high-GC) stack super-additively. cCRE supplement = 0.5765 eval_01
ceiling; GC-filter pushes eval_08 to 0.225 at cost of others. If
composite combines both gains, eval_01 could exceed 0.580.
"""
from pathlib import Path
import sys
import numpy as np
from pyfaidx import Fasta

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "006_dinuc_shuffled_multichrom"))
from generate import dinuc_shuffle  # noqa: E402

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_CCRE = 7_500
N_GCF = 7_500
GC_LO, GC_HI = 0.50, 0.80
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")

# mc5 baseline
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

# Type-balanced cCREs (then shuffled)
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
shuffled_ccres = [dinuc_shuffle(s, rng) for s in ccre_seqs]

# GC-filter supplement from mc5 chroms
chrom_lens = {c: len(fas[c][c]) for c in CHROMS}
chrom_weights = np.array([chrom_lens[c] for c in CHROMS], dtype=float)
chrom_weights /= chrom_weights.sum()
gcf = []
while len(gcf) < N_GCF:
    batch_size = 8 * (N_GCF - len(gcf))
    chrom_choices = rng.choice(len(CHROMS), size=batch_size, p=chrom_weights)
    for ci in chrom_choices:
        if len(gcf) >= N_GCF:
            break
        c = CHROMS[ci]
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = fas[c][c][start:start + L]
        if len(s) != L or not set(s).issubset(valid):
            continue
        gc = (s.count("G") + s.count("C")) / L
        if GC_LO <= gc <= GC_HI:
            gcf.append(s)

all_seqs = genomic + shuffled_ccres + gcf
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 7.5k shuf-cCRE + 7.5k GC-filter.")
