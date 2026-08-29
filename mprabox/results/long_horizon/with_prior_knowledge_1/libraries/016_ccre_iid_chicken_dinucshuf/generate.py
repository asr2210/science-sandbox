#!/usr/bin/env python3
"""
Experiment 016 — cCRE (35K) + iid (5K) + chicken (5K) + dinuc-shuffled
cCRE (5K), NO HUMAN-GEN.

Tests whether per-sequence dinucleotide-shuffled cCRE serve as a useful
5th axis (hard negatives) in a saturated 4-axis library. Replaces
human-gen with dinuc-shuffled cCRE — direct mirror of 014's drop-human
design.

Dinuc-shuffle: per-sequence Markov chain preserving dinucleotide
transition counts in expectation. Breaks trinuc+ structure (motifs)
while keeping dinucleotide frequencies intact. Strictly harder than
the mono-shuffled negatives tested in 005.

RNG: cCRE = seed*2+1, iid = seed*4+11, chicken-gen = seed*4+23,
dinuc-source-sample = seed*4+29, dinuc-shuffle = seed*4+31,
final shuffle = seed*4+17. human-gen (seed*4+13) and mouse-gen
(seed*4+19) streams omitted.
"""
from __future__ import annotations

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
N_PER_CLASS = 7_000
N_IID = 5_000
N_CHICKEN_GEN = 5_000
N_DINUC = 5_000
N_TOTAL = 50_000
PRIMARY_CLASSES = ("PLS", "pELS", "dELS", "CTCF-only", "DNase-H3K4me3")
CHICKEN_CHROMS = (
    tuple(f"chr{i}" for i in range(1, 29))
    + tuple(f"chr{i}" for i in range(30, 34))
    + ("chrW", "chrZ")
)
SEEDS = (0, 1, 2)


def primary_class(field6: str) -> str | None:
    head = field6.split(",", 1)[0]
    return head if head in PRIMARY_CLASSES else None


def load_cre_data():
    pools = {c: [] for c in PRIMARY_CLASSES}
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
    return pools


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


def sample_ccre(seed, pools, genome) -> tuple[list[str], set]:
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
    return seqs, used


def random_iid(seed, n) -> list[str]:
    rng = random.Random(seed * 4 + 11)
    return ["".join(rng.choices("ACGT", k=WIN)) for _ in range(n)]


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


def dinuc_shuffle(seq: str, rng: random.Random) -> str:
    """Per-sequence dinuc shuffle via Markov chain. Preserves dinucleotide
    transition counts in expectation; breaks all trinuc+ structure."""
    counts = {a: {b: 0 for b in "ACGT"} for a in "ACGT"}
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        counts[a][b] += 1
    out = [seq[0]]
    cur = seq[0]
    for _ in range(len(seq) - 1):
        cnt = counts[cur]
        total = cnt["A"] + cnt["C"] + cnt["G"] + cnt["T"]
        if total == 0:
            cur = rng.choice("ACGT")
        else:
            r = rng.randrange(total)
            for b in "ACGT":
                if r < cnt[b]:
                    cur = b
                    break
                r -= cnt[b]
        out.append(cur)
    return "".join(out)


def dinuc_shuffled_ccre(seed, n, pools, genome, used_keys) -> list[str]:
    """Sample n cCRE elements (disjoint from those used in the cCRE 35K),
    extract window, dinuc-shuffle each."""
    sample_rng = random.Random(seed * 4 + 29)
    shuf_rng = random.Random(seed * 4 + 31)
    flat_pool = []
    for cls in PRIMARY_CLASSES:
        flat_pool.extend(pools[cls])
    sample_rng.shuffle(flat_pool)
    seqs = []
    seen = set()
    for chrom, mid in flat_pool:
        if len(seqs) >= n:
            break
        key = (chrom, mid)
        if key in used_keys or key in seen:
            continue
        raw = extract_window(genome, chrom, mid - WIN // 2, sample_rng)
        if raw is None:
            continue
        seqs.append(dinuc_shuffle(raw, shuf_rng))
        seen.add(key)
    if len(seqs) < n:
        raise RuntimeError(f"dinuc-shuf: only {len(seqs)}/{n}")
    return seqs


def main() -> None:
    print("Loading cCRE data...", file=sys.stderr)
    pools = load_cre_data()
    print("Opening hg38 + galGal6 .2bit...", file=sys.stderr)
    hg38 = TwoBitFile(str(HG38))
    galgal6 = TwoBitFile(str(GALGAL6))
    for seed in SEEDS:
        print(f"\n[seed {seed}] cCRE 35K (7K x 5)...", file=sys.stderr)
        ccre, used = sample_ccre(seed, pools, hg38)
        print(f"[seed {seed}] iid 5K...", file=sys.stderr)
        iid = random_iid(seed, N_IID)
        print(f"[seed {seed}] chicken genomic 5K...", file=sys.stderr)
        cgen = random_chicken_genomic(seed, N_CHICKEN_GEN, galgal6)
        print(f"[seed {seed}] dinuc-shuffled cCRE 5K...", file=sys.stderr)
        dshuf = dinuc_shuffled_ccre(seed, N_DINUC, pools, hg38, used)
        seqs = ccre + iid + cgen + dshuf
        if len(seqs) != N_TOTAL:
            raise RuntimeError(f"seed {seed}: total {len(seqs)} != {N_TOTAL}")
        random.Random(seed * 4 + 17).shuffle(seqs)
        out_path = OUT_DIR / f"sequences_{seed}.txt"
        with open(out_path, "w") as fh:
            fh.write("\n".join(seqs) + "\n")
        print(f"[seed {seed}] wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
