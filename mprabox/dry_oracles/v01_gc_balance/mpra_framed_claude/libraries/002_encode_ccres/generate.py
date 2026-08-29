"""002_encode_ccres: 50,000 200bp windows centered on ENCODE GRCh38 cCREs.

Stratified sampling across cCRE types to maximize regulatory grammar diversity:
the model should see promoters (PLS), proximal enhancers (pELS), distal
enhancers (dELS), CTCF-bound elements, plain chromatin-accessible regions,
TF-bound, and H3K4me3-marked regions in roughly equal counts.

Rationale (generalization): a library that covers all major cCRE types exposes
the model to the full regulatory grammar that real cell types use, rather than
oversampling distal enhancers which dominate the pool. Motif → mechanism
mappings learned from PLS/CTCF/TF should transfer to unseen cell types better
than enhancer-only training would.
"""
import gzip
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 2

# Quotas per cCRE type
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
assert sum(QUOTA.values()) == N


def load_hg38(path):
    """Stream-load all chromosomes from a gz fasta into a dict {chrom: bytes}.

    Uppercases. Keeps only chr1..chr22, chrX, chrY (skip alt/random/chrM)."""
    keep = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    chroms = {}
    current_name = None
    current_chunks = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if current_name is not None and current_name in keep:
                    chroms[current_name] = "".join(current_chunks).upper()
                name = line[1:].split()[0]
                current_name = name
                current_chunks = []
            else:
                if current_name in keep:
                    current_chunks.append(line.rstrip())
        if current_name is not None and current_name in keep:
            chroms[current_name] = "".join(current_chunks).upper()
    return chroms


def load_ccres(path, keep_chroms):
    """Yield (chrom, start, end, ctype) for each line."""
    by_type = defaultdict(list)
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep_chroms:
                continue
            start = int(parts[1])
            end = int(parts[2])
            ctype = parts[9]
            by_type[ctype].append((chrom, start, end))
    return by_type


def extract_window(seq, mid, length):
    half = length // 2
    s = mid - half
    e = s + length
    if s < 0 or e > len(seq):
        return None
    win = seq[s:e]
    if "N" in win:
        return None
    return win


def main():
    print("Loading hg38...", flush=True)
    chroms = load_hg38(HG38_FA_GZ)
    print(f"  loaded {len(chroms)} chromosomes, total {sum(len(s) for s in chroms.values())/1e9:.2f} Gb", flush=True)

    print("Loading cCREs...", flush=True)
    by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    for k, v in by_type.items():
        print(f"  {k}: {len(v):>8d}", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []
    for ctype, quota in QUOTA.items():
        pool = by_type[ctype]
        # Shuffle and walk through, accepting until we hit quota
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= quota:
                break
            chrom, start, end = pool[idx]
            mid = (start + end) // 2
            win = extract_window(chroms[chrom], mid, L)
            if win is None:
                continue
            assert len(win) == L
            assert set(win) <= set("ACGT")
            seqs.append(win)
            added += 1
        print(f"  {ctype}: got {added}/{quota}", flush=True)
        if added < quota:
            print(f"  WARN: short on {ctype}", flush=True)

    assert len(seqs) == N, f"got {len(seqs)} != {N}"
    rng.shuffle(seqs)  # shuffle order so cCRE types are interleaved
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"Wrote {len(seqs)} sequences to {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
