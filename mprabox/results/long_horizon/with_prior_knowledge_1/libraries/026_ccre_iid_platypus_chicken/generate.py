#!/usr/bin/env python3
"""
Experiment 026 — platypus replaces human-gen.

Library: 35K cCRE (7K each across 5 classes) + 5K iid (uniform) +
5K platypus genomic (ornAna2) + 5K chicken (galGal6) = 50K.

Replaces 010's human-gen (~+0.005 value) with platypus genomic.
Tests "evolutionary distance" theory of chicken's superior fourth-
component value:
  - Mouse (~96 Mya from human, mammal): paired with chicken in 013
    → mean 0.7945 (worse than 010 by ~0.011).
  - Chicken (~310 Mya, bird): proven best 4th component in 010.
  - Platypus (~166 Mya, monotreme — most distant living mammal):
    UNTESTED. Sits between mouse and chicken on the tree.

Predictions:
  - "Evolutionary distance from human" theory: platypus should sit
    between mouse and chicken in 4th-component value. With chicken
    held at 5K, platypus + chicken stacking ≈ mouse + chicken
    stacking (i.e., 026 < 010, by ~0.005-0.020).
  - "Bird-architecture special" theory: platypus is mammalian and
    similar in regulatory grammar to mouse → 026 ≈ 013, mean ~0.79.
  - "Cross-species axis caps at 1 species regardless" theory:
    026 ≈ 010 within ±0.005 (the 5K platypus contributes the same
    as 5K human-gen; saturation already reached via chicken).

Platypus chromosome list: named chr contigs from ornAna2 with size
≥ 1Mb (excludes the chr20_AAPN01103024v1_random sliver and 200K+
unplaced scaffolds). Total bp: ~437M (similar order to galGal6).

RNG: cCRE = seed*2+1, iid = seed*4+11, platypus-gen = seed*4+13
(replaces human-gen RNG, same offset), chicken-gen = seed*4+23,
final shuffle = seed*4+17.
"""
from __future__ import annotations

import bisect
import random
import sys
from pathlib import Path

from twobitreader import TwoBitFile

REPO = Path(__file__).resolve().parents[2]
CCRE_BED = REPO / "data" / "cCRE" / "GRCh38-cCREs.bed"
HG38 = REPO / "data" / "genome" / "hg38.2bit"
GALGAL6 = REPO / "data" / "genome" / "galGal6.2bit"
ORNANA2 = REPO / "data" / "genome" / "ornAna2.2bit"
OUT_DIR = Path(__file__).resolve().parent

WIN = 200
N_PER_CLASS = 7_000
N_IID = 5_000
N_PLATYPUS_GEN = 5_000
N_CHICKEN_GEN = 5_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
HUMAN_CHROMS = tuple(f"chr{i}" for i in range(1, 23)) + ("chrX",)
CHICKEN_CHROMS = (
    tuple(f"chr{i}" for i in range(1, 29))
    + tuple(f"chr{i}" for i in range(30, 34))
    + ("chrW", "chrZ")
)
PLATYPUS_CHROMS = (
    "chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7",
    "chr10", "chr11", "chr12", "chr14", "chr15", "chr17",
    "chr18", "chr20", "chrX1", "chrX2", "chrX3", "chrX5",
)
SEEDS = (0, 1, 2)
CCRE_EXCLUSION_BP = 200


def primary_class(field6: str) -> str | None:
    head = field6.split(",", 1)[0]
    return head if head in PRIMARY_CLASSES else None


def load_cre_data():
    pools = {c: [] for c in PRIMARY_CLASSES}
    intervals = {}
    with open(CCRE_BED) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            cls = primary_class(parts[5])
            if cls is not None:
                mid = (start + end) // 2
                pools[cls].append((chrom, mid))
            intervals.setdefault(chrom, []).append((start, end))
    for chrom in intervals:
        intervals[chrom].sort()
    return pools, intervals


def overlaps_cre(chrom, start, end, intervals) -> bool:
    chr_intervals = intervals.get(chrom)
    if chr_intervals is None:
        return False
    s = start - CCRE_EXCLUSION_BP
    e = end + CCRE_EXCLUSION_BP
    starts = [iv[0] for iv in chr_intervals]
    idx = bisect.bisect_right(starts, e)
    i = idx - 1
    while i >= 0:
        iv_start, iv_end = chr_intervals[i]
        if iv_end <= s:
            break
        if iv_start < e and iv_end > s:
            return True
        i -= 1
    return False


def extract_window(genome, chrom, start, rng) -> str | None:
    end = start + WIN
    chrom_len = len(genome[chrom])
    if start < 0 or end > chrom_len:
        return None
    seq = genome[chrom][start:end].upper()
    if len(seq) != WIN:
        return None
    if seq.count("N") > WIN // 2:
        return None
    return "".join(b if b in "ACGT" else rng.choice("ACGT") for b in seq)


def sample_ccre(seed, pools, genome) -> list[str]:
    rng = random.Random(seed * 2 + 1)
    seqs = []
    used = set()
    for cls in PRIMARY_CLASSES:
        pool = pools[cls]
        order = list(range(len(pool)))
        rng.shuffle(order)
        kept = 0
        for idx in order:
            if kept >= N_PER_CLASS:
                break
            chrom, mid = pool[idx]
            key = (chrom, mid)
            if key in used:
                continue
            seq = extract_window(genome, chrom, mid - WIN // 2, rng)
            if seq is None:
                continue
            seqs.append(seq)
            used.add(key)
            kept += 1
        if kept < N_PER_CLASS:
            raise RuntimeError(f"seed {seed}: {cls} only produced {kept}/{N_PER_CLASS}")
    return seqs


def random_iid(seed, n) -> list[str]:
    rng = random.Random(seed * 4 + 11)
    return ["".join(rng.choices("ACGT", k=WIN)) for _ in range(n)]


def random_platypus_genomic(seed, n, genome) -> list[str]:
    rng = random.Random(seed * 4 + 13)
    chroms = list(PLATYPUS_CHROMS)
    chrom_lens = {c: len(genome[c]) for c in chroms}
    cum, csum = [], 0
    for c in chroms:
        csum += chrom_lens[c]
        cum.append(csum)
    total = csum
    seqs = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 50:
            raise RuntimeError(f"platypus-gen: only {len(seqs)}/{n}")
        x = rng.randrange(total)
        ci = 0
        while x >= cum[ci]:
            ci += 1
        chrom = chroms[ci]
        prev = cum[ci - 1] if ci > 0 else 0
        pos = x - prev
        start = pos - WIN // 2
        end = start + WIN
        if start < 0 or end > chrom_lens[chrom]:
            continue
        seq = extract_window(genome, chrom, start, rng)
        if seq is None:
            continue
        seqs.append(seq)
    return seqs


def random_chicken_genomic(seed, n, genome) -> list[str]:
    rng = random.Random(seed * 4 + 23)
    chroms = list(CHICKEN_CHROMS)
    chrom_lens = {c: len(genome[c]) for c in chroms}
    cum, csum = [], 0
    for c in chroms:
        csum += chrom_lens[c]
        cum.append(csum)
    total = csum
    seqs = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 50:
            raise RuntimeError(f"chicken-gen: only {len(seqs)}/{n}")
        x = rng.randrange(total)
        ci = 0
        while x >= cum[ci]:
            ci += 1
        chrom = chroms[ci]
        prev = cum[ci - 1] if ci > 0 else 0
        pos = x - prev
        start = pos - WIN // 2
        end = start + WIN
        if start < 0 or end > chrom_lens[chrom]:
            continue
        seq = extract_window(genome, chrom, start, rng)
        if seq is None:
            continue
        seqs.append(seq)
    return seqs


def main() -> None:
    print("Loading cCRE data...", file=sys.stderr)
    pools, intervals = load_cre_data()
    print("Opening hg38 + galGal6 + ornAna2 .2bit...", file=sys.stderr)
    hg38 = TwoBitFile(str(HG38))
    galgal6 = TwoBitFile(str(GALGAL6))
    ornana2 = TwoBitFile(str(ORNANA2))
    for seed in SEEDS:
        print(f"\n[seed {seed}] cCRE 35K (7K x 5)...", file=sys.stderr)
        ccre = sample_ccre(seed, pools, hg38)
        print(f"[seed {seed}] iid 5K...", file=sys.stderr)
        iid = random_iid(seed, N_IID)
        print(f"[seed {seed}] platypus genomic 5K...", file=sys.stderr)
        pgen = random_platypus_genomic(seed, N_PLATYPUS_GEN, ornana2)
        print(f"[seed {seed}] chicken genomic 5K...", file=sys.stderr)
        cgen = random_chicken_genomic(seed, N_CHICKEN_GEN, galgal6)
        seqs = ccre + iid + pgen + cgen
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        random.Random(seed * 4 + 17).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
