"""003_ccre_random_mix: 25k ENCODE cCREs + 25k uniform random 200bp.

Tests whether mixing random sequences with real cCREs restores eval_08
(which got worse with pure cCREs) while preserving the eval_01 gains.

Generalization rationale: pairs natural regulatory grammar (cCREs) with
broad sequence-composition coverage (random), so the model is in-distribution
for either real or synthetic test sequences, regardless of cell type.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 25000
N_RAND = 25000
RNG_SEED = 3
ALPHABET = np.array(list("ACGT"))

# cCRE quotas (half of exp 002)
QUOTA = {
    "PLS":        3000,
    "pELS":       3500,
    "dELS":       5000,
    "TF":         3000,
    "CA":         3000,
    "CA-CTCF":    3000,
    "CA-H3K4me3": 2500,
    "CA-TF":      2000,
}
assert sum(QUOTA.values()) == N_CCRE


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
            chrom = parts[0]
            if chrom not in keep:
                continue
            by_type[parts[9]].append((chrom, int(parts[1]), int(parts[2])))
    return by_type


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

    rng = np.random.default_rng(RNG_SEED)
    seqs = []

    # cCRE arm
    for ctype, quota in QUOTA.items():
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
        print(f"  {ctype}: {added}/{quota}", flush=True)

    # Random arm
    idx = rng.integers(0, 4, size=(N_RAND, L), dtype=np.int8)
    rand = ALPHABET[idx]
    for row in rand:
        seqs.append("".join(row.tolist()))

    assert len(seqs) == N_CCRE + N_RAND, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
