"""007_dhs_index_stratified: 50k DHS sites stratified across 16 tissue components.

Uses the Meuleman 2020 DHS index (3.6M elements with biosample counts,
mean DNase signal, summit coords, and tissue-component assignments).

Stratification rationale (generalization): components span the major
tissue/cell-lineage groups (neural, lymphoid, cardiac, hepatic, embryonic,
etc.). Sampling evenly across components teaches the model regulatory
grammar that operates in every lineage, not just the three measured
biosamples (K562 = myeloid/erythroid, HepG2 = digestive/cancer, SK-N-SH =
neural). This is a direct play on cross-cell-type generalization.

Sampling: per component, sample 50000/16 elements, with a weighting toward
higher numsamples (broader / more reproducible elements) using probability
∝ log(1 + numsamples). Center 200bp window on the DHS summit.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
DHS_PATH = f"{ROOT}/data/dhs/DHS_Index.txt.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 7


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


def load_dhs(path, keep):
    """Returns dict {component: list of (chrom, summit, numsamples)}."""
    by_comp = defaultdict(list)
    with gzip.open(path, "rt") as fh:
        header = fh.readline()  # skip header
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            summit = int(parts[6])
            numsamples = int(parts[5])
            comp = parts[9]
            by_comp[comp].append((chrom, summit, numsamples))
    return by_comp


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
    print("Loading DHS index...", flush=True)
    by_comp = load_dhs(DHS_PATH, set(chroms.keys()))
    for k, v in by_comp.items():
        print(f"  {k:35s} {len(v):>8d}", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    components = sorted(by_comp.keys())
    per_comp = N // len(components)
    leftover = N - per_comp * len(components)
    quotas = {c: per_comp for c in components}
    for c in components[:leftover]:
        quotas[c] += 1
    assert sum(quotas.values()) == N

    seqs = []
    for comp, quota in quotas.items():
        pool = by_comp[comp]
        # Probability weighted by log(1 + numsamples)
        ns = np.array([p[2] for p in pool], dtype=np.float64)
        weights = np.log1p(ns)
        weights = weights / weights.sum()
        # Oversample to allow rejects
        n_try = min(len(pool), int(quota * 3))
        idx_pool = rng.choice(len(pool), size=n_try, replace=False, p=weights)
        added = 0
        for idx in idx_pool:
            if added >= quota:
                break
            chrom, summit, _ = pool[idx]
            win = extract(chroms[chrom], summit, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  {comp:35s} {added}/{quota}", flush=True)

    assert len(seqs) == N, f"got {len(seqs)} != {N}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
