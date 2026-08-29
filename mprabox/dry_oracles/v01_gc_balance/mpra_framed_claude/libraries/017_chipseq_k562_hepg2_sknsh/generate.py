"""017_chipseq_k562_hepg2_sknsh: 50k TF ChIP-seq peaks in target cell types.

ENCODE TF binding clusters (encRegTfbsClusteredWithCells.hg38, 10.5M entries)
contain (chrom, start, end, TF, score, cell_type) tuples for TF ChIP-seq
peaks across many cell types and TFs. I filter to entries observed in
K562 / HepG2 / SK-N-SH and take 17k / 17k / 16k unique-locus peaks.

Why ChIP-seq peaks could break the cCRE ceiling:
- cCREs are biochemical signatures (DNase+H3K4me3/CTCF/etc) that *suggest*
  regulatory potential. ChIP-seq peaks are *direct evidence* of TF binding
  in the specific cell type. They mark the actual functional sites used
  by the cell's TF repertoire.
- A K562 ChIP-seq peak is, by construction, a TF-bound regulatory site in
  K562. cCREs are broader and include sites that may not be active in K562.

Selection:
1. Stream the ChIP-seq bed; for each row, if cell-type field contains
   K562 / HepG2 / SK-N-SH (substring match handles comma-separated multi-CT
   entries), assign the peak midpoint to that cell's pool.
2. Per pool, dedupe by 200bp genomic bin so we don't oversample co-bound
   clusters.
3. Sample 17k / 17k / 16k from the three pools and extract 200bp windows.

Generalization rationale: TF binding sites are the most direct evidence
of regulatory function. The motif syntax around bound peaks is exactly
what a cell-type-specific activity model needs to learn. If 50k cCREs
ceiling at 0.69, this should at minimum match and might break the ceiling.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CHIP_BED = f"{ROOT}/data/chipseq/encRegTfbsClusteredWithCells.hg38.bed.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
BIN = 200  # dedupe resolution
RNG_SEED = 17
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


def load_chip_by_cell(path, keep):
    pools = {ct: set() for ct in TARGETS}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            cell_field = parts[5]
            for ct in TARGETS:
                if ct in cell_field:
                    pools[ct].add((chrom, mid // BIN))
    return {ct: list(pool) for ct, pool in pools.items()}


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
    pools = load_chip_by_cell(CHIP_BED, set(chroms.keys()))
    for ct, pool in pools.items():
        print(f"  {ct}: {len(pool)} unique 200bp bins", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []
    for ct, target_n in TARGETS.items():
        pool = pools[ct]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= target_n:
                break
            chrom, bin_id = pool[idx]
            mid = bin_id * BIN + BIN // 2
            win = extract(chroms[chrom], mid, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  pool {ct}: {added}/{target_n}", flush=True)

    assert len(seqs) == sum(TARGETS.values()), f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
