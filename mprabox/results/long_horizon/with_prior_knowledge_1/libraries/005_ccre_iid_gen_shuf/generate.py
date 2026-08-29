#!/usr/bin/env python3
"""
Experiment 005 — cCRE (35K) + iid (5K) + genomic windows (5K) + mononucleotide-
shuffled genomic (5K).

Tests whether adding a THIRD qualitatively distinct sequence source extends
the iid+genomic synergy observed in exp 004.

The mononucleotide-shuffled component is each genomic window with its bases
randomly permuted: it preserves the per-window base composition (so its
average composition matches the human genome's ~29A / 21C / 21G / 29T) but
DESTROYS dinucleotide and higher-order motif structure entirely.

It sits cleanly between iid (uniform 25/25/25/25, no composition structure)
and real genomic (composition + dinuc + motifs + repeats). A clean test of
whether "realistic mono composition WITHOUT motifs/dinucs" carries any
training signal beyond what iid and real genomic already contribute.
"""
from __future__ import annotations

import bisect
import random
import sys
from pathlib import Path

from twobitreader import TwoBitFile

REPO = Path(__file__).resolve().parents[2]
CCRE_BED = REPO / "data" / "cCRE" / "GRCh38-cCREs.bed"
GENOME = REPO / "data" / "genome" / "hg38.2bit"
OUT_DIR = Path(__file__).resolve().parent

WIN = 200
N_PER_CLASS = 7_000
N_IID = 5_000
N_GENOMIC = 5_000
N_SHUFFLED = 5_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
AUTOSOMES_PLUS_X = tuple(f"chr{i}" for i in range(1, 23)) + ("chrX",)
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
    for c in PRIMARY_CLASSES:
        print(f"  pool[{c}] = {len(pools[c]):,}", file=sys.stderr)
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
    rng = random.Random(seed * 2 + 1)  # SAME stream as 002/003/004
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
    rng = random.Random(seed * 4 + 11)  # SAME stream as 004's iid
    return ["".join(rng.choices("ACGT", k=WIN)) for _ in range(n)]


def random_genomic(seed, n, intervals, genome, rng_stream_offset=13) -> list[str]:
    rng = random.Random(seed * 4 + rng_stream_offset)
    chrom_lens = {c: len(genome[c]) for c in AUTOSOMES_PLUS_X}
    cum, csum = [], 0
    chroms = list(AUTOSOMES_PLUS_X)
    for c in chroms:
        csum += chrom_lens[c]
        cum.append(csum)
    total = csum
    seqs = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 50:
            raise RuntimeError(f"only {len(seqs)}/{n} after {attempts} attempts")
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
        if overlaps_cre(chrom, start, end, intervals):
            continue
        seq = extract_window(genome, chrom, start, rng)
        if seq is None:
            continue
        seqs.append(seq)
    return seqs


def mono_shuffle(seq: str, rng: random.Random) -> str:
    """Random permutation of bases within seq. Preserves per-window base
    counts; destroys all dinucleotide and higher-order structure."""
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)


def sample_shuffled_genomic(seed, n, intervals, genome) -> list[str]:
    """Sample n DIFFERENT genomic windows (separate RNG from the real-genomic
    component) and mono-shuffle each in place."""
    shuf_rng = random.Random(seed * 4 + 29)
    real = random_genomic(seed, n, intervals, genome, rng_stream_offset=23)
    return [mono_shuffle(s, shuf_rng) for s in real]


def main() -> None:
    print("Loading cCRE data...", file=sys.stderr)
    pools, intervals = load_cre_data()
    print("Opening hg38.2bit...", file=sys.stderr)
    genome = TwoBitFile(str(GENOME))
    for seed in SEEDS:
        print(f"\n[seed {seed}] cCRE 35K (7K x 5)...", file=sys.stderr)
        ccre = sample_ccre(seed, pools, genome)
        print(f"[seed {seed}] iid 5K...", file=sys.stderr)
        iid = random_iid(seed, N_IID)
        print(f"[seed {seed}] real genomic 5K...", file=sys.stderr)
        gen = random_genomic(seed, N_GENOMIC, intervals, genome, rng_stream_offset=13)
        print(f"[seed {seed}] mono-shuffled genomic 5K...", file=sys.stderr)
        shuf = sample_shuffled_genomic(seed, N_SHUFFLED, intervals, genome)
        seqs = ccre + iid + gen + shuf
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        random.Random(seed * 4 + 17).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
