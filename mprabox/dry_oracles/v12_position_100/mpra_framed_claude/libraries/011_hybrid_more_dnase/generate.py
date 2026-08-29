"""Experiment 011: Composition tilt — more DNase, less cCRE.

010 showed adding H3K27ac as a 3rd source dilutes the productive ones.
009 (20K cCRE + 25K DNase + 5K random) is the current best.
This experiment tests whether shifting MORE toward DNase improves further:
- 15K cCREs (down from 20K)
- 30K DNase peaks (10K per cell, up from 25K)
- 5K random

Hypothesis: cell-type-specific DNase signal still has room. Cutting cCRE
share by 5K and giving those slots to per-cell DNase should sharpen
per-cell prediction while keeping enough cCRE for cross-tissue grammar.

If 011 > 009: more DNase still helps; can push further (exp 012: tilt more)
If 011 < 009: 009 is sweet spot, pivot to qualitatively new sources
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
DNASE_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 11

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    6_000,
    "pELS":    4_000,
    "PLS":     2_000,
    "CA_TF":   1_500,
    "CA-CTCF": 1_500,
}
DNASE_TARGET = 10_000
N_RANDOM = 5_000


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccres(path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def parse_peaks(path):
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            start, end = int(parts[1]), int(parts[2])
            try: so = int(parts[9])
            except (ValueError, IndexError): so = -1
            summit = (start + so) if so >= 0 else (start + end) // 2
            yield chrom, summit


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class = {k: [] for k in CCRE_TARGETS}
    for chrom, s, e, t in parse_ccres(CCRE_BED):
        if t == "PLS": grp = "PLS"
        elif t == "pELS": grp = "pELS"
        elif t == "dELS": grp = "dELS"
        elif t == "CA-CTCF": grp = "CA-CTCF"
        else: grp = "CA_TF"
        by_class[grp].append((chrom, (s + e) // 2))

    seqs = []
    seen = set()

    for grp, target in CCRE_TARGETS.items():
        pool = by_class[grp]
        rng.shuffle(pool)
        added = 0
        for chrom, center in pool:
            if added >= target:
                break
            ws, we = window_around_center(center)
            if ws < 0 or we > contig_lens[chrom]:
                continue
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  cCRE {grp}: {added}/{target}")

    for cell, path in DNASE_FILES.items():
        peaks = list(parse_peaks(path))
        rng.shuffle(peaks)
        added = 0
        for chrom, summit in peaks:
            if added >= DNASE_TARGET:
                break
            ws, we = window_around_center(summit)
            if ws < 0 or we > contig_lens[chrom]:
                continue
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  DNase {cell}: {added}/{DNASE_TARGET}")

    chrom_list = sorted(AUTOSOMES, key=lambda c: int(c[3:]))
    w = np.array([contig_lens[c] for c in chrom_list], dtype=float)
    w /= w.sum()
    added = 0
    tries = 0
    while added < N_RANDOM and tries < 200_000:
        tries += 1
        chrom = nprng.choice(chrom_list, p=w)
        clen = contig_lens[chrom]
        start = int(nprng.integers(0, clen - L))
        seq = fetch_clean(fa, chrom, start, start + L)
        if seq is None:
            continue
        key = (chrom, start)
        if key in seen:
            continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  random: {added}/{N_RANDOM} ({tries} tries)")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} != {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
