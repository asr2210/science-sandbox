"""005_ccre_rc_jitter: 50k cCREs with positional jitter + RC augmentation.

Same stratified cCRE mix as exp 002 but with two augmentations applied per
sequence:
1. Window center jittered uniformly within ±50bp of cCRE midpoint
   (teaches positional invariance — real test sequences won't have motifs
   perfectly centered).
2. 50% probability of reverse-complementing the resulting window
   (teaches strand invariance — DNA is double-stranded).

Generalization rationale: cell-type-specific motif activity is
strand-invariant and position-invariant in real regulatory elements; a
model that learns these invariances should transfer to any cell type's
elements regardless of how they're framed in the eval input.
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
JITTER = 50
RNG_SEED = 5

QUOTA = {
    "PLS":        6000,
    "pELS":       7000,
    "dELS":      10000,
    "TF":         6000,
    "CA":         6000,
    "CA-CTCF":    6000,
    "CA-H3K4me3": 5000,
    "CA-TF":      4000,
}
assert sum(QUOTA.values()) == 50000

RC = str.maketrans("ACGT", "TGCA")


def revcomp(s):
    return s.translate(RC)[::-1]


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
    for ctype, quota in QUOTA.items():
        pool = by_type[ctype]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= quota:
                break
            chrom, start, end = pool[idx]
            mid = (start + end) // 2 + int(rng.integers(-JITTER, JITTER + 1))
            win = extract(chroms[chrom], mid, L)
            if win is None:
                continue
            if rng.random() < 0.5:
                win = revcomp(win)
            seqs.append(win)
            added += 1
        print(f"  {ctype}: {added}/{quota}", flush=True)

    assert len(seqs) == 50000
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
