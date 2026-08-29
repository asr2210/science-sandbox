#!/usr/bin/env python3
"""
Experiment 021 — iid composition test. Library: 35K cCRE 7K-each + 5K
hg38-mononucleotide-matched iid + 5K human + 5K chicken = 50K.

Mirrors 010 exactly except the iid component uses hg38 mononucleotide
frequencies (sampled from hg38 chr22 — fixed, reproducible) instead of
uniform 25% per base. Probes whether iid value is composition-agnostic
(off-genome anchor) or composition-dependent.

hg38 mononuc freq (computed at runtime from chr1, deterministic;
chr1 is the longest autosome and ~42% GC, close to whole-genome 41%).

RNG: identical streams to 010. cCRE = seed*2+1, iid = seed*4+11,
human-gen = seed*4+13, chicken-gen = seed*4+23, final shuffle = seed*4+17.
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
OUT_DIR = Path(__file__).resolve().parent

WIN = 200
N_BY_CLASS = {
    "PLS": 7_000,
    "pELS": 7_000,
    "dELS": 7_000,
    "CTCF-only": 7_000,
    "DNase-H3K4me3": 7_000,
}
N_IID = 5_000
N_HUMAN_GEN = 5_000
N_CHICKEN_GEN = 5_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
HUMAN_CHROMS = tuple(f"chr{i}" for i in range(1, 23)) + ("chrX",)
CHICKEN_CHROMS = (
    tuple(f"chr{i}" for i in range(1, 29))
    + tuple(f"chr{i}" for i in range(30, 34))
    + ("chrW", "chrZ")
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
        n_target = N_BY_CLASS[cls]
        if n_target == 0:
            continue
        pool = pools[cls]
        order = list(range(len(pool)))
        rng.shuffle(order)
        kept = 0
        for idx in order:
            if kept >= n_target:
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
        if kept < n_target:
            raise RuntimeError(f"seed {seed}: {cls} only produced {kept}/{n_target}")
    return seqs


def compute_hg38_mononuc(genome) -> tuple[float, float, float, float]:
    """Compute (pA, pC, pG, pT) from hg38 chr1 (deterministic, ~250 Mb,
    representative of whole-genome composition ~41% GC)."""
    seq = genome["chr1"][:].upper()
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        if b in counts:
            counts[b] += 1
    total = sum(counts.values())
    return (
        counts["A"] / total,
        counts["C"] / total,
        counts["G"] / total,
        counts["T"] / total,
    )


def random_iid_hg38_matched(seed, n, weights) -> list[str]:
    rng = random.Random(seed * 4 + 11)
    return ["".join(rng.choices("ACGT", weights=weights, k=WIN)) for _ in range(n)]


def random_human_genomic(seed, n, intervals, genome) -> list[str]:
    rng = random.Random(seed * 4 + 13)
    chrom_lens = {c: len(genome[c]) for c in HUMAN_CHROMS}
    cum, csum = [], 0
    for c in HUMAN_CHROMS:
        csum += chrom_lens[c]
        cum.append(csum)
    total = csum
    seqs = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 50:
            raise RuntimeError(f"human-gen: only {len(seqs)}/{n}")
        x = rng.randrange(total)
        ci = 0
        while x >= cum[ci]:
            ci += 1
        chrom = HUMAN_CHROMS[ci]
        prev = cum[ci - 1] if ci > 0 else 0
        pos = x - prev
        start = pos - WIN // 2
        end = start + WIN
        if start < 0 or end > chrom_lens[chrom]:
            continue
        if overlaps_cre(chrom, start, end, intervals):
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
    print("Opening hg38 + galGal6 .2bit...", file=sys.stderr)
    hg38 = TwoBitFile(str(HG38))
    galgal6 = TwoBitFile(str(GALGAL6))
    print("Computing hg38 mononuc freq from chr1...", file=sys.stderr)
    pA, pC, pG, pT = compute_hg38_mononuc(hg38)
    print(f"  hg38 mononuc: A={pA:.4f} C={pC:.4f} G={pG:.4f} T={pT:.4f} "
          f"(GC={pC+pG:.4f})", file=sys.stderr)
    weights = [pA, pC, pG, pT]
    for seed in SEEDS:
        print(f"\n[seed {seed}] cCRE 35K (7K-each)...", file=sys.stderr)
        ccre = sample_ccre(seed, pools, hg38)
        print(f"[seed {seed}] iid 5K (hg38-mononuc-matched)...", file=sys.stderr)
        iid = random_iid_hg38_matched(seed, N_IID, weights)
        print(f"[seed {seed}] human genomic 5K...", file=sys.stderr)
        hgen = random_human_genomic(seed, N_HUMAN_GEN, intervals, hg38)
        print(f"[seed {seed}] chicken genomic 5K...", file=sys.stderr)
        cgen = random_chicken_genomic(seed, N_CHICKEN_GEN, galgal6)
        seqs = ccre + iid + hgen + cgen
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        random.Random(seed * 4 + 17).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
