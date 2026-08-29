"""Experiment 020: Pure cCRE library with ALL 8 classes proportionally.

Until now my cCRE sampling grouped {CA, TF, CA-H3K4me3, CA-TF} into one
"CA_TF" bucket. The Registry V4 actually has 8 classes:
  dELS 1.47M, pELS 249K, CA 246K, CA-CTCF 126K, TF 105K,
  CA-H3K4me3 79K, PLS 47K, CA-TF 26K

This experiment samples ALL 8 classes proportionally to natural prevalence
(within each class). Tests whether being explicit about CA-H3K4me3 / TF /
CA classes — which have distinct chromatin signatures — improves the
sequence-grammar exposure.

50K total, no peaks, no random:
- 17K dELS (34% – capped, natural ~60%)
- 6K pELS
- 6K CA
- 5K CA-CTCF
- 5K TF
- 5K CA-H3K4me3
- 4K PLS
- 2K CA-TF
= 50K. Seed=20.

Tests if pure cCRE diversity (broader class set) beats hybrid (009).
"""
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 20

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":        17_000,
    "pELS":         6_000,
    "CA":           6_000,
    "CA-CTCF":      5_000,
    "TF":           5_000,
    "CA-H3K4me3":   5_000,
    "PLS":          4_000,
    "CA-TF":        2_000,
}


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_ccres(path):
    by_class = {}
    for line in open(path):
        parts = line.rstrip("\n").split("\t")
        chrom = parts[0]
        if chrom not in AUTOSOMES: continue
        s, e, t = int(parts[1]), int(parts[2]), parts[5]
        by_class.setdefault(t, []).append((chrom, (s + e) // 2))
    return by_class


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def main():
    rng = random.Random(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs (all classes)...")
    by_class = parse_ccres(CCRE_BED)
    for k, v in sorted(by_class.items(), key=lambda kv: -len(kv[1])):
        print(f"  pool {k}: {len(v)}")

    seqs = []
    seen = set()
    for grp, target in CCRE_TARGETS.items():
        pool = by_class.get(grp, [])
        rng.shuffle(pool)
        added = 0
        for chrom, center in pool:
            if added >= target: break
            ws, we = window_around_center(center)
            if ws < 0 or we > contig_lens[chrom]: continue
            key = (chrom, ws)
            if key in seen: continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None: continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  cCRE {grp}: {added}/{target}")

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
