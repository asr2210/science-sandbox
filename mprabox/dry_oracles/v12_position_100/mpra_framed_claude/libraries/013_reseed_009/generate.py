"""Experiment 013: REPLICATE of 009 with SEED=13 to measure noise floor.

Same composition as 009 (20K cCRE + 25K DNase + 5K random), different seed.
Tells us whether 010/011/012's ~0.0015 regression from 009 is real signal
or pipeline noise.

Original 009 docstring follows.
---
Experiment 009: Hybrid library — cCREs + cell-type DNase peaks + random.

50,000 sequences combining the best of broad regulatory diversity
(cCREs across many cell types) with cell-type-targeted accessibility
(DNase peaks in our 3 measured cell types).

Composition:
- 20K cCREs (8K dELS + 5K pELS + 3K PLS + 2K CA_TF + 2K CA-CTCF)
- 8K K562 DNase peaks (peak-summit centered)
- 8K HepG2 DNase peaks
- 9K SK-N-SH DNase peaks   (slightly extra to compensate SKNSH gap)
- 5K random non-cCRE autosomal background

Hypothesis: the cCRE half teaches broad regulatory grammar (transferable
across cell types) and the DNase half sharpens cell-type-specific
prediction in the 3 measured cells. The random background gives
"null" examples that anchor the model's activity calibration.

If 009 > 008 and 009 > 003: hybrid is best — go further this direction.
If only 009 > 008: cCRE diversity is better; drop the cell-type focus.
If only 009 > 003: cell-type focus is better; drop the cCREs.
If 009 ≈ 008 ≈ 003: 0.076-ish plateau is hard architectural cap.

Generalization argument: the cCRE portion provides regulatory grammar
exposure useful for any cell type. The cell-type DNase portion is
relevant only for the 3 measured cells but those cells are part of the
eval. Net effect should be positive on eval_01 if the two signals are
complementary.
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"
PEAK_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 13

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    8_000,
    "pELS":    5_000,
    "PLS":     3_000,
    "CA_TF":   2_000,
    "CA-CTCF": 2_000,
}
DNASE_TARGETS = {"K562": 8_000, "HepG2": 8_000, "SKNSH": 9_000}
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
            if chrom not in AUTOSOMES:
                continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def parse_peaks(path):
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            start, end = int(parts[1]), int(parts[2])
            try:
                so = int(parts[9])
            except (ValueError, IndexError):
                so = -1
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

    for cell, target in DNASE_TARGETS.items():
        peaks = list(parse_peaks(PEAK_FILES[cell]))
        rng.shuffle(peaks)
        added = 0
        for chrom, summit in peaks:
            if added >= target:
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
        print(f"  DNase {cell}: {added}/{target}")

    # Random autosomal background
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
