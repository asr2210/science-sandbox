"""Experiment 018: phastCons conserved elements substituting cCRE.

20K natural + 15K phastCons-centered + 10K DHS + 5K mouse.

Phylogenetic conservation (100-species phastCons) is an orthogonal
selection criterion to chromatin accessibility. Conserved elements
include:
- enhancers under purifying selection
- splice sites and RNA structure regions
- ultraconserved noncoding elements (UCNEs)
- many regions not flagged by cCRE/DHS

Hypothesis: conserved-but-not-open and conserved-and-open are both
functionally important but represent different feature classes. Adding
conservation-selected sequences exposes the model to functional sequences
that chromatin atlases miss.

If 018 > 0.508 (>2σ above plateau), conservation provides orthogonal
signal. If equal, conservation overlaps with chromatin atlases at the
model level.

phastConsElements100way.txt.gz format: bin chrom start end "lod=N" score.
Score is 0-1000, LOD reflects evidence for conservation.
We filter for LOD≥50 (strong evidence) to focus on truly conserved.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_PHASTCONS = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_PHASTCONS - N_DHS
L = 200
SEED = 0
MIN_LOD = 50  # filter for strongly conserved elements

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
PHASTCONS = os.path.join(REPO_ROOT, "data", "phastcons.txt.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HUMAN_SET = set(HUMAN_CHROMS)


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


def sample_phastcons(fa, n, rng):
    """Center 200bp window on phastCons element midpoint, with small offset."""
    elements = []
    with gzip.open(PHASTCONS, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            # cols: bin chrom start end lod_str score
            if len(parts) < 6:
                continue
            chrom = parts[1]
            if chrom not in HUMAN_SET:
                continue
            try:
                lod = int(parts[4].split("=", 1)[1])
            except (ValueError, IndexError):
                continue
            if lod < MIN_LOD:
                continue
            start = int(parts[2])
            end = int(parts[3])
            mid = (start + end) // 2
            elements.append((chrom, mid))
    print(f"phastCons elements LOD>={MIN_LOD}: {len(elements)}")
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        # small offset to provide window-position variation (like cCRE off-center)
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
    natural = sample_natural(hg, HUMAN_CHROMS, N_NATURAL, rng)
    phastcons = sample_phastcons(hg, N_PHASTCONS, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + phastcons + dhs + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} phastcons={len(phastcons)} dhs={len(dhs)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
