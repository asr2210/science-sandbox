"""Experiment 024: GC + CpG joint-matched mc5 supplement (v2).

35k mc5 + 15k mc5 windows that match cCRE's GC histogram AND have CpG
density boosted via within-bin selection of CpG-richer candidates.

Pure rejection-sampling of (GC,CpG) joint is infeasible because mc5
random has very few high-CpG windows. Instead: for each GC bin, sample
many candidates and keep the ones with highest CpG to approximate the
cCRE CpG distribution within that bin.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_SUPP = N - N_GENOMIC
N_GC_BINS = 20
GC_RANGE = (0.20, 0.80)
OVERSAMPLE = 5  # collect 5x target per bin to allow CpG selection
DATA = Path(__file__).resolve().parents[2] / "data"
BED = DATA / "GRCh38-cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")
chrom_set = set(CHROMS)


def gc_cpg(s):
    gc = (s.count("G") + s.count("C")) / L
    cpg = sum(1 for i in range(L - 1) if s[i] == "C" and s[i + 1] == "G")
    return gc, cpg


def gc_to_bin(gc):
    b = int((gc - GC_RANGE[0]) / (GC_RANGE[1] - GC_RANGE[0]) * N_GC_BINS)
    return min(max(b, 0), N_GC_BINS - 1)


# 1) cCRE distribution: per-GC-bin target count and per-bin median CpG
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

per_type_target = N_SUPP // 5
ccre_bin_stats = [[] for _ in range(N_GC_BINS)]  # list of CpG values per bin
all_ccre_cpgs = []
all_ccre_gcs = []
for t, pool in ccres_by_type.items():
    idx = rng.choice(len(pool), size=min(len(pool), 4 * per_type_target), replace=False)
    count = 0
    for i in idx:
        if count >= per_type_target:
            break
        chrom, mid = pool[i]
        start, end = mid - HALF, mid - HALF + L
        if start < 0 or end > len(fas[chrom][chrom]):
            continue
        s = fas[chrom][chrom][start:end]
        if len(s) == L and set(s).issubset(valid):
            gc, cpg = gc_cpg(s)
            ccre_bin_stats[gc_to_bin(gc)].append(cpg)
            all_ccre_cpgs.append(cpg)
            all_ccre_gcs.append(gc)
            count += 1

bin_target_counts = np.array([len(b) for b in ccre_bin_stats])
bin_target_cpgs = np.array([np.mean(b) if b else 0 for b in ccre_bin_stats])
total = bin_target_counts.sum()
print(f"cCRE GC: mean={np.mean(all_ccre_gcs):.3f}")
print(f"cCRE CpG count per 200bp: mean={np.mean(all_ccre_cpgs):.2f}, "
      f"std={np.std(all_ccre_cpgs):.2f}")

# Scale targets to sum to N_SUPP
scaled = (bin_target_counts.astype(float) / total * N_SUPP).astype(int)
deficit = N_SUPP - scaled.sum()
if deficit > 0:
    biggest = np.argsort(-bin_target_counts)[:deficit]
    for b in biggest:
        scaled[b] += 1
assert scaled.sum() == N_SUPP

# 2) Collect mc5 window candidates per GC bin
chrom_lens = {c: len(fas[c][c]) for c in CHROMS}
chrom_weights = np.array([chrom_lens[c] for c in CHROMS], dtype=float)
chrom_weights /= chrom_weights.sum()

candidates = [[] for _ in range(N_GC_BINS)]
batch_size = 100_000
attempts = 0
needed_candidate_count = scaled * OVERSAMPLE
print(f"Targets per bin (×oversample={OVERSAMPLE}):", needed_candidate_count)
while any(len(candidates[b]) < needed_candidate_count[b]
          for b in range(N_GC_BINS) if scaled[b] > 0):
    chrom_choices = rng.choice(len(CHROMS), size=batch_size, p=chrom_weights)
    for ci in chrom_choices:
        c = CHROMS[ci]
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = fas[c][c][start:start + L]
        if len(s) != L or not set(s).issubset(valid):
            continue
        gc, cpg = gc_cpg(s)
        if gc < GC_RANGE[0] or gc >= GC_RANGE[1]:
            continue
        b = gc_to_bin(gc)
        if scaled[b] == 0:
            continue
        if len(candidates[b]) < needed_candidate_count[b]:
            candidates[b].append((s, cpg))
    attempts += 1
    if attempts > 30:
        print(f"Stopping after {attempts} batches; some bins under-collected")
        break

print(f"Candidate counts per bin: {[len(c) for c in candidates]}")

# 3) For each bin, pick the top-CpG `scaled[b]` candidates
supp = []
chosen_cpgs = []
for b in range(N_GC_BINS):
    if scaled[b] == 0:
        continue
    pool = candidates[b]
    if len(pool) < scaled[b]:
        # not enough — take all and pad with duplicates
        sorted_pool = sorted(pool, key=lambda x: -x[1])
        sel = sorted_pool + list(rng.choice(sorted_pool, size=scaled[b] - len(pool),
                                            replace=True))
    else:
        # top-CpG selection
        sorted_pool = sorted(pool, key=lambda x: -x[1])
        sel = sorted_pool[:scaled[b]]
    for s, cpg in sel:
        supp.append(s)
        chosen_cpgs.append(cpg)

assert len(supp) == N_SUPP

# 4) mc5 baseline (35k)
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

supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in supp])
print(f"Supp GC: mean={supp_gcs.mean():.3f}, std={supp_gcs.std():.3f}")
print(f"Supp CpG: mean={np.mean(chosen_cpgs):.2f} "
      f"(cCRE mean = {np.mean(all_ccre_cpgs):.2f})")

all_seqs = genomic + supp
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 15k mc5 (GC-matched, top-CpG within bin).")
