"""010_ccre_unstratified: 50k cCREs sampled uniformly from full ENCODE pool.

No type stratification. Lets the natural cCRE distribution dominate:
~62% dELS (distal enhancers), ~11% pELS, ~10% CA, ~5% CA-CTCF,
~4.5% TF, ~3% CA-H3K4me3, ~2% PLS, ~1% CA-TF.

Hypothesis: my exp 002 stratification under-samples dELS (the most common
class) and over-samples PLS/pELS/CA-TF. If dELS carries the most
generalizable regulatory grammar in the bulk eval data, unstratified
should match or beat exp 002.

Generalization rationale: dELS represent the bulk of distal regulatory
elements active across cell types. Letting them dominate (in proportion
to their genomic frequency) mirrors the real distribution of regulatory
elements the model would encounter in any cell-type prediction task.
"""
import gzip
import os

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 10


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
    cres = []
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            cres.append((parts[0], int(parts[1]), int(parts[2]), parts[9]))
    return cres


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
    cres = load_ccres(CCRE_BED, set(chroms.keys()))
    print(f"  total cCREs loaded: {len(cres)}", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    order = rng.permutation(len(cres))
    seqs = []
    type_counts = {}
    for idx in order:
        if len(seqs) >= N:
            break
        chrom, start, end, ctype = cres[idx]
        win = extract(chroms[chrom], (start + end) // 2, L)
        if win is None:
            continue
        seqs.append(win)
        type_counts[ctype] = type_counts.get(ctype, 0) + 1

    for k in sorted(type_counts.keys()):
        print(f"  {k:12s} {type_counts[k]:>6d}", flush=True)

    assert len(seqs) == N
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
