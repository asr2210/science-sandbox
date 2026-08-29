"""027_ccre_fantom_malinois: 17k cCRE + 17k FANTOM5 + 16k Malinois.

Drop ChIP-seq from the 3-source mega-pool, replace with FANTOM5 CAGE
peaks. Tests whether FANTOM5 can substitute for ChIP-seq in the
diversity-mix recipe.

Exp 018 (cCRE+ChIP+Malinois 17/17/16): 0.6928
Exp 025 (4-source with FANTOM5):       0.6928 (eval_04 lift)
This (cCRE+FANTOM5+Malinois 17/17/16): ?

If 0.6928, FANTOM5 substitutes for ChIP-seq cleanly — both are
"3rd-source" qualifiers and any biological regulatory source works.
If higher, FANTOM5 carries more eval_01 signal per sequence than ChIP.
If lower, ChIP-seq contributes specifically.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
CAGE_BED = f"{ROOT}/data/fantom/cage_peaks.bed.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 17000
N_CAGE = 17000
N_MPRA = 16000
RNG_SEED = 27

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
    chroms = load_hg38(HG38_FA_GZ, keep)
    ccres_by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    cage = load_cage(CAGE_BED, set(chroms.keys()))
    mpra = load_malinois(MPRA_PATH)

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

    idx_mp = rng.choice(len(mpra), size=N_MPRA, replace=False)
    seqs.extend(mpra[i] for i in idx_mp)
    print(f"  Malinois: {N_MPRA}", flush=True)

    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
