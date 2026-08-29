"""Experiment 019: GC-stratified natural sampling.

Same exp 011 structure but the 20K natural component is sampled
uniformly across 6 GC bins instead of by random genomic position.

GC bins: [0.15, 0.30), [0.30, 0.40), [0.40, 0.50), [0.50, 0.60),
[0.60, 0.70), [0.70, 0.85). ~3,333 sequences per bin.

Random natural has bimodal GC (isochores 40-50% + CpG islands 60-70%);
extreme bins are under-sampled. Forcing uniform exposes model to GC-
extreme contexts (AT-rich heterochromatin, very-GC-rich CpG islands).

Hypothesis: better GC-space coverage helps model generalize to GC-
extreme regulatory regions in held-out evals. If 019 > 0.508, GC
coverage is a real lever.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CCRE = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_CCRE - N_DHS
L = 200
SEED = 0

GC_BINS = [(0.15, 0.30), (0.30, 0.40), (0.40, 0.50),
           (0.50, 0.60), (0.60, 0.70), (0.70, 0.85)]
PER_BIN = N_NATURAL // len(GC_BINS)
LEFTOVER = N_NATURAL - PER_BIN * len(GC_BINS)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HUMAN_SET = set(HUMAN_CHROMS)
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}


def gc(s):
    return (s.count("G") + s.count("C")) / len(s)


def sample_natural_gc_stratified(fa, chroms, n, rng, max_attempts=10_000_000):
    """Sample equal numbers across GC bins."""
    chrom_lens = {c: len(fa[c]) for c in chroms}
    arr = np.array(chroms)
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    targets = [PER_BIN] * len(GC_BINS)
    for i in range(LEFTOVER):
        targets[i] += 1
    bins = [[] for _ in GC_BINS]
    attempts = 0
    while sum(len(b) for b in bins) < n and attempts < max_attempts:
        attempts += 1
        c = rng.choice(arr, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        g = gc(s)
        for i, (lo, hi) in enumerate(GC_BINS):
            if lo <= g < hi and len(bins[i]) < targets[i]:
                bins[i].append(s)
                break
    print(f"GC-bin counts (attempts={attempts}): "
          f"{[len(b) for b in bins]} / target {targets}")
    out = []
    for b in bins:
        out.extend(b)
    return out


def sample_natural(fa, chroms, n, rng):
    chrom_lens = {c: len(fa[c]) for c in chroms}
    arr = np.array(chroms)
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(arr, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def sample_offcenter_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET or parts[9] not in HIGH_CONF:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((parts[0], mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        offset = int(rng.integers(25, 176))
        start = mid - offset
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def sample_dhs(fa, n, rng):
    summits = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET:
                continue
            summits.append((parts[0], int(parts[6])))
    idx = rng.permutation(len(summits))
    out = []
    for i in idx:
        chrom, mid = summits[i]
        start = mid - L // 2
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def main():
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)
    natural = sample_natural_gc_stratified(hg, HUMAN_CHROMS, N_NATURAL, rng)
    ccre = sample_offcenter_ccre(hg, N_CCRE, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + ccre + dhs + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} ccre={len(ccre)} dhs={len(dhs)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
