"""022_chipseq_highconf: 50k high-confidence ChIP-seq peaks (top by score).

Exp 017 used uniform random ChIP-seq peaks; this experiment selects the
top-scoring (most confidently bound) peaks per cell type. Hypothesis:
high-confidence peaks have stronger TF binding evidence, so the model
sees cleaner regulatory grammar per sequence.

Per CT: keep one peak per 200bp bin (highest-score wins on collision),
then take top 17k (K562, HepG2) / 16k (SK-N-SH) by score.

ChIP-seq score distribution (column 5 in encRegTfbsClustered):
  min 2, p50 343, p95 1000, max 1000 (saturated cap).
The top quartile (score > 590) is the "well-bound" subset.

Generalization rationale: a TF cluster bound with high confidence is
more likely to be a true active regulatory site than a low-score peak.
Less noise per sequence → more learnable signal in the same 50k budget.
"""
import gzip
import os

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CHIP_BED = f"{ROOT}/data/chipseq/encRegTfbsClusteredWithCells.hg38.bed.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
RNG_SEED = 22
TARGETS = {"K562": 17000, "HepG2": 17000, "SK-N-SH": 16000}


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


def load_chip_by_cell_scored(path, keep):
    pools = {ct: {} for ct in TARGETS}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            score = int(parts[4])
            cell_field = parts[5]
            for ct in pools:
                if ct in cell_field:
                    key = (chrom, mid // 200)
                    if score > pools[ct].get(key, 0):
                        pools[ct][key] = score
    return pools


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
    pools = load_chip_by_cell_scored(CHIP_BED, set(chroms.keys()))
    for ct, pool in pools.items():
        print(f"  {ct}: {len(pool)} unique bins", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []
    for ct, target in TARGETS.items():
        items = list(pools[ct].items())
        items.sort(key=lambda x: -x[1])  # high score first
        added = 0
        for (chrom, bin_id), score in items:
            if added >= target:
                break
            mid = bin_id * 200 + 100
            win = extract(chroms[chrom], mid, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  {ct}: kept {added}/{target}", flush=True)

    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
