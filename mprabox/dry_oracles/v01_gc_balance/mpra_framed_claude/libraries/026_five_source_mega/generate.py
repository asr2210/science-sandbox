"""026_five_source_mega: 10k each cCRE + ChIP + Malinois + FANTOM5 + DHS.

Tests whether adding DHS as a 5th source on top of the 4-source FANTOM5
mega-pool (exp 025) helps or dilutes. Exp 021 showed DHS as a 4th
source hurt the 3-source mega-pool slightly. Maybe with FANTOM5 also
present, DHS is more complementary.

Recipe: 10k cCRE + 10k ChIP + 10k Malinois + 10k FANTOM5 + 10k DHS.

Hypothesis: if eval_01 stays at 0.6928, more diversity = same ceiling.
If it drops, DHS still dilutes regardless of other sources present.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
CHIP_BED = f"{ROOT}/data/chipseq/encRegTfbsClusteredWithCells.hg38.bed.gz"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
CAGE_BED = f"{ROOT}/data/fantom/cage_peaks.bed.gz"
DHS_PATH = f"{ROOT}/data/dhs/DHS_Index.txt.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
RNG_SEED = 26

N_EACH = 10000
CCRE_QUOTA = {
    "PLS":        1200,
    "pELS":       1400,
    "dELS":       2000,
    "TF":         1200,
    "CA":         1200,
    "CA-CTCF":    1200,
    "CA-H3K4me3": 1000,
    "CA-TF":       800,
}
assert sum(CCRE_QUOTA.values()) == N_EACH

CHIP_TARGETS = {"K562": 3400, "HepG2": 3400, "SK-N-SH": 3200}
assert sum(CHIP_TARGETS.values()) == N_EACH


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


def load_chip_by_cell(path, keep):
    pools = {ct: set() for ct in CHIP_TARGETS}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            cell_field = parts[5]
            for ct in pools:
                if ct in cell_field:
                    pools[ct].add((chrom, mid // 200))
    return {ct: list(pool) for ct, pool in pools.items()}


def load_malinois(path):
    seqs = []
    with open(path) as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            s = parts[11]
            if len(s) != L:
                continue
            if any(c not in "ACGT" for c in s):
                continue
            seqs.append(s)
    return seqs


def load_cage(path, keep):
    out = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            out.append((parts[0], mid))
    return out


def load_dhs(path, keep, min_ns=5):
    out = []
    with gzip.open(path, "rt") as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            if int(parts[5]) < min_ns:
                continue
            summit = int(parts[6])
            out.append((chrom, summit))
    return out


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
    chroms = load_hg38(HG38_FA_GZ, keep)
    ccres_by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    chip_pools = load_chip_by_cell(CHIP_BED, set(chroms.keys()))
    mpra = load_malinois(MPRA_PATH)
    cage = load_cage(CAGE_BED, set(chroms.keys()))
    dhs = load_dhs(DHS_PATH, set(chroms.keys()))

    rng = np.random.default_rng(RNG_SEED)
    seqs = []

    for ctype, quota in CCRE_QUOTA.items():
        pool = ccres_by_type[ctype]
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

    for ct, target in CHIP_TARGETS.items():
        pool = chip_pools[ct]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= target:
                break
            chrom, bin_id = pool[idx]
            mid = bin_id * 200 + 100
            win = extract(chroms[chrom], mid, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  ChIP {ct}: {added}/{target}", flush=True)

    idx_mp = rng.choice(len(mpra), size=N_EACH, replace=False)
    seqs.extend(mpra[i] for i in idx_mp)
    print(f"  Malinois: {N_EACH}", flush=True)

    order = rng.permutation(len(cage))
    added = 0
    for idx in order:
        if added >= N_EACH:
            break
        chrom, mid = cage[idx]
        win = extract(chroms[chrom], mid, L)
        if win is None:
            continue
        seqs.append(win)
        added += 1
    print(f"  CAGE: {added}/{N_EACH}", flush=True)

    order = rng.permutation(len(dhs))
    added = 0
    for idx in order:
        if added >= N_EACH:
            break
        chrom, summit = dhs[idx]
        win = extract(chroms[chrom], summit, L)
        if win is None:
            continue
        seqs.append(win)
        added += 1
    print(f"  DHS: {added}/{N_EACH}", flush=True)

    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
