"""011_ccre_multitile: 25k unique cCREs × 2 windows each at offsets {-50, +50}.

Tests if dense per-element sampling (2 distinct framings of the same
regulatory element) gives the model better signal than 50k unique cCREs
(1 framing each). Total stays at 50,000 sequences.

Two windows per cCRE at midpoint−50 and midpoint+50 each contain most of
the cCRE element but with different positional context — left-shifted vs
right-shifted view. The model can learn the same regulatory grammar from
both views, similar to augmentation but with systematic coverage.

Generalization rationale: If multi-view per element is what the model is
limited by (rather than number of unique elements), then this should win.
The data tells the model "this motif arrangement should produce this
activity, regardless of where in the input window it sits."
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
N_UNIQUE = 25000
OFFSETS = [-50, +50]
RNG_SEED = 11

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
assert sum(QUOTA.values()) == N_UNIQUE


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
    chroms = load_hg38(HG38_FA_GZ, keep)
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
            base_mid = (start + end) // 2
            wins = []
            ok = True
            for off in OFFSETS:
                w = extract(chroms[chrom], base_mid + off, L)
                if w is None:
                    ok = False
                    break
                wins.append(w)
            if not ok:
                continue
            seqs.extend(wins)
            added += 1
        print(f"  {ctype}: {added}/{quota}", flush=True)

    assert len(seqs) == N_UNIQUE * len(OFFSETS), f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
