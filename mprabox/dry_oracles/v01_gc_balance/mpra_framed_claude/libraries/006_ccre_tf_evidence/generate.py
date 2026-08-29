"""006_ccre_tf_evidence: 50k cCREs filtered to TF-evidence types only.

Sample from PLS (promoter-like), pELS (proximal enhancer), TF (TF-bound),
CA-TF (chromatin-accessible + TF-bound). Drops the bulk dELS distal-enhancer
class and the weaker CA-only / CA-CTCF / CA-H3K4me3 classes.

Hypothesis: TF-evidence cCREs are the highest-confidence regulatory elements
and may concentrate more learnable signal per sequence than the
type-stratified mix that includes weaker classes.

Generalization rationale: TF-evidence elements are where DNA→TF→activity
mechanism is best supported across many cell types. Training the model on
the cleanest examples of this mechanism should transfer to unseen cell types
because TF binding biology is conserved.
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
RNG_SEED = 6

# Quotas across TF-evidence cCRE types (sums to 50000)
QUOTA = {
    "PLS":   12000,   # 47k pool — concentrated promoters
    "pELS":  18000,   # 249k pool — proximal enhancers
    "TF":    14000,   # 105k pool — TF-bound regions
    "CA-TF":  6000,   #  26k pool — TF-bound chromatin accessible
}
assert sum(QUOTA.values()) == 50000


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
            win = extract(chroms[chrom], (start + end) // 2, L)
            if win is None:
                continue
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
