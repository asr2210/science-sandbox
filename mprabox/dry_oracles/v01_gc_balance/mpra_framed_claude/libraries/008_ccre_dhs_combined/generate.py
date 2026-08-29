"""008_ccre_dhs_combined: 25k cCREs + 25k DHS sites.

Combines ENCODE cCREs (strong, well-curated regulatory annotation matched to
the labeled cell types) with Meuleman DHS sites (broader, more biosample
coverage). Tests if the union of two regulatory data sources produces a
more informative library than either alone.

Generalization rationale: cCREs and DHS use different selection criteria
and so capture overlapping but distinct slices of regulatory grammar.
Mixing them exposes the model to a wider set of motifs / architectures /
chromatin contexts than either source. Even if some DHS sites are
cell-type-specific to non-measured tissues, their motif content should
help the model build a richer TF-binding vocabulary that transfers to
unseen cell types.

Design:
- 25k cCREs (stratified across 8 types, halved exp 002 quotas, seed=8)
- 25k DHS sites (uniform random from DHS index, summit-centered window),
  filtered for numsamples >= 5 to drop singleton noise
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
DHS_PATH = f"{ROOT}/data/dhs/DHS_Index.txt.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 25000
N_DHS = 25000
RNG_SEED = 8
MIN_NUMSAMPLES = 5

CCRE_QUOTA = {
    "PLS":        3000,
    "pELS":       3500,
    "dELS":       5000,
    "TF":         3000,
    "CA":         3000,
    "CA-CTCF":    3000,
    "CA-H3K4me3": 2500,
    "CA-TF":      2000,
}
assert sum(CCRE_QUOTA.values()) == N_CCRE


def load_hg38(path, keep):
    chroms = {}; cur = None; chunks = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if cur and cur in keep:
                    chroms[cur] = "".join(chunks).upper()
                cur = line[1:].split()[0]; chunks = []
            elif cur in keep:
                chunks.append(line.rstrip())
        if cur in keep:
            chroms[cur] = "".join(chunks).upper()
    return chroms


def load_ccres(path, keep):
    by_type = defaultdict(list)
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            by_type[parts[9]].append((parts[0], int(parts[1]), int(parts[2])))
    return by_type


def load_dhs(path, keep, min_ns):
    dhs = []
    with gzip.open(path, "rt") as fh:
        fh.readline()  # header
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            ns = int(parts[5])
            if ns < min_ns:
                continue
            dhs.append((parts[0], int(parts[6])))  # chrom, summit
    return dhs


def extract(seq, mid, length):
    half = length // 2
    s = mid - half; e = s + length
    if s < 0 or e > len(seq):
        return None
    win = seq[s:e]
    if "N" in win:
        return None
    return win


def main():
    keep = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    print("Loading hg38...", flush=True)
    chroms = load_hg38(HG38_FA_GZ, keep)
    print("Loading cCREs...", flush=True)
    by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    print("Loading DHS (numsamples >= 5)...", flush=True)
    dhs = load_dhs(DHS_PATH, set(chroms.keys()), MIN_NUMSAMPLES)
    print(f"  {len(dhs)} DHS sites loaded", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []

    # cCRE arm
    for ctype, quota in CCRE_QUOTA.items():
        pool = by_type[ctype]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= quota:
                break
            chrom, start, end = pool[idx]
            win = extract(chroms[chrom], (start + end) // 2, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  cCRE {ctype}: {added}/{quota}", flush=True)

    # DHS arm
    order = rng.permutation(len(dhs))
    added = 0
    for idx in order:
        if added >= N_DHS:
            break
        chrom, summit = dhs[idx]
        win = extract(chroms[chrom], summit, L)
        if win is None:
            continue
        seqs.append(win)
        added += 1
    print(f"  DHS: {added}/{N_DHS}", flush=True)

    assert len(seqs) == N_CCRE + N_DHS, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
