"""023_mega_rc_jitter: 3-source mega-pool with RC and per-element jitter.

Same recipe as exp 020 (cCRE-heavy 30/10/10 mega-pool) but with two
augmentations:
1. cCRE / ChIP windows: jitter ±50bp before extraction (different positional
   framing of each element).
2. Every sequence: 50% probability of reverse-complementing.

Exp 005 (cCRE + RC + jitter alone) showed no lift over plain cCREs.
But the 3-source mega-pool exposed slightly more grammar; maybe
augmentation interacts non-additively with source diversity.

Hypothesis: if the mega-pool was on the brink of needing more diverse
*positional/strand* views to use its broader motif coverage, RC+jitter
could squeeze a bit more out. If not, this matches exp 020 (0.6928).

Generalization rationale: positional/strand augmentation forces the
model to learn motif content independent of where in the window the
motif sits and which strand it's on. Combined with source-diversity
mega-pool, the model sees the maximum coverage of regulatory grammar.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
CHIP_BED = f"{ROOT}/data/chipseq/encRegTfbsClusteredWithCells.hg38.bed.gz"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
JIT = 50
N_CCRE = 30000
N_CHIP = 10000
N_MPRA = 10000
RNG_SEED = 23

CCRE_QUOTA = {
    "PLS":        3500,
    "pELS":       4500,
    "dELS":       6500,
    "TF":         3500,
    "CA":         3500,
    "CA-CTCF":    3000,
    "CA-H3K4me3": 3000,
    "CA-TF":      2500,
}
assert sum(CCRE_QUOTA.values()) == N_CCRE

CHIP_TARGETS = {"K562": 3400, "HepG2": 3400, "SK-N-SH": 3200}
assert sum(CHIP_TARGETS.values()) == N_CHIP

RCTAB = str.maketrans("ACGT", "TGCA")


def rc(s):
    return s.translate(RCTAB)[::-1]


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


def load_chip_by_cell(path, keep):
    pools = {ct: set() for ct in CHIP_TARGETS}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            cell_field = parts[5]
            for ct in pools:
                if ct in cell_field:
                    pools[ct].add((chrom, mid // 200))
    return {ct: list(pool) for ct, pool in pools.items()}


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
    chip_pools = load_chip_by_cell(CHIP_BED, set(chroms.keys()))
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
            base_mid = (start + end) // 2
            off = int(rng.integers(-JIT, JIT + 1))
            win = extract(chroms[chrom], base_mid + off, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  cCRE {ctype}: {added}/{quota}", flush=True)

    for ct, target in CHIP_TARGETS.items():
        pool = chip_pools[ct]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= target:
                break
            chrom, bin_id = pool[idx]
            mid = bin_id * 200 + 100
            off = int(rng.integers(-JIT, JIT + 1))
            win = extract(chroms[chrom], mid + off, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  ChIP {ct}: {added}/{target}", flush=True)

    idx_mp = rng.choice(len(mpra), size=N_MPRA, replace=False)
    seqs.extend(mpra[i] for i in idx_mp)
    print(f"  Malinois: {N_MPRA}", flush=True)

    # RC half
    rc_mask = rng.random(len(seqs)) < 0.5
    seqs = [rc(s) if rc_mask[i] else s for i, s in enumerate(seqs)]

    assert len(seqs) == 50000, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
