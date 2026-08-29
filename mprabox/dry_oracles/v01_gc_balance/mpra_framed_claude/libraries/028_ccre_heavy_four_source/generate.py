"""028_ccre_heavy_four_source: cCRE-heavy 4-source mega-pool with FANTOM5.

Tests if a cCRE-majority 4-source mix preserves the eval_04 lift from
FANTOM5 (best at 0.6220 in exp 027, 0.6197 in exp 025) while keeping
eval_01 at the 0.6928 ceiling.

Recipe: 25k cCRE + 8.5k ChIP + 8.5k Malinois + 8k FANTOM5.

Hypothesis: cCRE majority preserves eval_01 max (0.6928); minority
ChIP/Malinois/FANTOM5 mix provides enough diversity to also lift
eval_04 vs pure cCRE.

This is the candidate "best practice" 4-source recipe that should
optimize both eval_01 and eval_04 simultaneously.
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
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 25000
N_CHIP = 8500
N_MPRA = 8500
N_CAGE = 8000
RNG_SEED = 28

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

CHIP_TARGETS = {"K562": 2900, "HepG2": 2900, "SK-N-SH": 2700}
assert sum(CHIP_TARGETS.values()) == N_CHIP


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

    idx_mp = rng.choice(len(mpra), size=N_MPRA, replace=False)
    seqs.extend(mpra[i] for i in idx_mp)
    print(f"  Malinois: {N_MPRA}", flush=True)

    order = rng.permutation(len(cage))
    added = 0
    for idx in order:
        if added >= N_CAGE:
            break
        chrom, mid = cage[idx]
        win = extract(chroms[chrom], mid, L)
        if win is None:
            continue
        seqs.append(win)
        added += 1
    print(f"  CAGE: {added}/{N_CAGE}", flush=True)

    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
