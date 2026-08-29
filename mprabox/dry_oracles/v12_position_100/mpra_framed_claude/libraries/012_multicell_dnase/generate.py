"""Experiment 012: Multi-cell DNase diversity.

009 (best, 0.0772) used DNase from only the 3 measured cells.
010/011 confirmed: more sources or more DNase WITHIN those cells doesn't help.

This experiment adds DNase peaks from 3 NON-MEASURED cell types
(GM12878 lymphoblast, A549 lung carcinoma, HCT116 colon carcinoma).
Hypothesis: exposing the model to MORE cell-type regulatory contexts
strengthens its learning of UNIVERSAL TF motif features, which transfer
to unseen cells (the goal stated in instructions).

Composition (50K total):
- 15K cCREs (broad regulatory grammar, cross-tissue)
- 15K DNase from measured cells (5K each K562/HepG2/SKNSH)
- 15K DNase from non-measured cells (5K each GM12878/A549/HCT116)
- 5K random autosomal background

If 012 > 009: cell-type diversity helps generalization — push further
   (more cells, replace cCREs with more diverse DNase)
If 012 ≈ 009: diversity from cCREs already covers the cell-type range
If 012 < 009: adding off-target DNase dilutes the signal for measured cells
   (suggests focus on measured cells is necessary)
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
CCRE_BED = ROOT / "data" / "cCREs.bed"

# narrowPeak format (10 cols), summit = start + int(col 9)
DNASE_NP = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
# hotspot3 format (8 cols, header), summit = int(col 6), absolute
DNASE_H3 = {
    "GM12878": ROOT / "data" / "GM12878_dnase.bed.gz",
    "A549":    ROOT / "data" / "A549_dnase.bed.gz",
    "HCT116":  ROOT / "data" / "HCT116_dnase.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 12

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    6_000,
    "pELS":    4_000,
    "PLS":     2_000,
    "CA_TF":   1_500,
    "CA-CTCF": 1_500,
}
DNASE_TARGET = 5_000
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


def parse_narrowpeak(path):
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


def parse_hotspot3(path):
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES: continue
            try: summit = int(parts[6])
            except (ValueError, IndexError):
                start, end = int(parts[1]), int(parts[2])
                summit = (start + end) // 2
            yield chrom, summit


def window_around_center(center):
    s = center - L // 2
    return s, s + L


def sample_peaks_to(seqs, seen, fa, contig_lens, peaks, target, label, seed):
    rng = random.Random(seed)
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
    print(f"  {label}: {added}/{target}")
    return added


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

    for i, (cell, path) in enumerate(DNASE_NP.items()):
        peaks = list(parse_narrowpeak(path))
        sample_peaks_to(seqs, seen, fa, contig_lens, peaks,
                        DNASE_TARGET, f"DNase {cell}", SEED + 100 + i)

    for i, (cell, path) in enumerate(DNASE_H3.items()):
        peaks = list(parse_hotspot3(path))
        sample_peaks_to(seqs, seen, fa, contig_lens, peaks,
                        DNASE_TARGET, f"DNase {cell} (unmeasured)", SEED + 200 + i)

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
