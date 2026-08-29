"""018_mega_pool_three_source: 17k cCRE + 17k ChIP-seq + 16k Malinois MPRA.

Three qualitatively different regulatory-sequence sources, each contributing
roughly one third. Tests whether maximum-diversity mixing breaks the 0.69
eval_01 ceiling that's been observed across each source individually.

Sources:
1. cCREs (17k): biochemical regulatory annotation, stratified by type
2. ChIP-seq peaks (17k): direct TF binding evidence in K562/HepG2/SK-N-SH
3. Random Malinois MPRA (16k): real MPRA-measured oligos in the target CTs

Each source has hit ~0.69 individually:
  - exp 002 cCRE: 0.6921
  - exp 017 ChIP: 0.6900
  - exp 012 Malinois random: 0.6856

If the ceiling is *intrinsic* (model/eval bound), this hits ~0.69 too.
If the ceiling is from *redundancy within each source*, the union has
more diverse motif arrangements and could lift slightly.

Generalization rationale: a maximum-diversity multi-source library
should give the best out-of-distribution generalization because the
model sees regulatory grammar from biochemical, binding, and functional
angles. Worth one careful test even if it doesn't lift eval_01.
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
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 17000
N_CHIP = 17000
N_MPRA = 16000
RNG_SEED = 18

CCRE_QUOTA = {
    "PLS":        2000,
    "pELS":       2500,
    "dELS":       3500,
    "TF":         2000,
    "CA":         2000,
    "CA-CTCF":    2000,
    "CA-H3K4me3": 1500,
    "CA-TF":      1500,
}
assert sum(CCRE_QUOTA.values()) == N_CCRE

CHIP_PER_CT = N_CHIP // 3 + 1  # 5667; we'll trim to fit


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
    pools = {"K562": set(), "HepG2": set(), "SK-N-SH": set()}
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
    ccres_by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    print("Loading ChIP-seq...", flush=True)
    chip_pools = load_chip_by_cell(CHIP_BED, set(chroms.keys()))
    print("Loading Malinois...", flush=True)
    mpra = load_malinois(MPRA_PATH)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []

    # cCRE
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
    n_ccre = len(seqs)

    # ChIP-seq per cell
    chip_added = 0
    chip_target = N_CHIP
    for ct in ["K562", "HepG2", "SK-N-SH"]:
        pool = chip_pools[ct]
        order = rng.permutation(len(pool))
        per_target = chip_target // 3 if ct != "SK-N-SH" else chip_target - 2 * (chip_target // 3)
        added = 0
        for idx in order:
            if added >= per_target:
                break
            chrom, bin_id = pool[idx]
            mid = bin_id * 200 + 100
            win = extract(chroms[chrom], mid, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        chip_added += added
        print(f"  ChIP {ct}: {added}/{per_target}", flush=True)

    # Malinois fill
    idx_mp = rng.choice(len(mpra), size=N_MPRA, replace=False)
    seqs.extend(mpra[i] for i in idx_mp)
    print(f"  Malinois added: {N_MPRA}", flush=True)

    assert len(seqs) == n_ccre + chip_added + N_MPRA, f"got {len(seqs)}"
    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
