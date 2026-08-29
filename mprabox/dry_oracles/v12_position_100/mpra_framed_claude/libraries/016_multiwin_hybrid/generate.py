"""Experiment 016: Multi-window augmentation on 009 hybrid composition.

009 (cCRE + DNase + random) is the best single-window design. Composition
tweaks have plateaued in the noise band 0.072-0.077. Try a different axis:
positional augmentation. Each regulatory locus contributes 3 shifted
200bp windows (offsets −100, 0, +100 from the locus center/summit).

Unique loci ~16.7K with 3 windows each = 50K sequences.
- 6.7K cCREs × 3 windows = 20K cCRE-derived
- 8.3K DNase loci × 3 windows = 25K DNase-derived (across 3 cells)
- 5K random (single-window each)

Hypothesis: showing the model the same regulatory element at 3 positions
teaches it to extract motif features regardless of where in the 200bp
window they fall. May improve generalization to held-out sequences whose
motifs are shifted differently.

Exp 007 tried this on cCREs only (50K = 16.7K cCREs × 3 windows) and got
0.0747 (within noise of cCRE single-window 0.0758). Combining with
the productive hybrid mix tests whether augmentation interacts with
the cell-type signal.

If 016 ≥ 0.080: multi-window augmentation helps; explore 5 windows
If 016 ∈ [0.073, 0.078]: in noise band, augmentation also doesn't help
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
SEED = 16

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

# Each locus = 3 windows. Total seqs = unique_loci * 3.
CCRE_TARGETS = {
    "dELS":    2_700,
    "pELS":    1_700,
    "PLS":     1_000,
    "CA_TF":   700,
    "CA-CTCF": 700,
}  # ~6.8K loci × 3 windows = ~20.4K
DNASE_TARGET = 2_700  # × 3 cells × 3 windows = 24.3K
N_RANDOM = 5_000  # single window
WINDOW_OFFSETS = [-100, 0, 100]  # shifts in bp from center


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


def add_multiwindow(seqs, seen, fa, contig_lens, loci, target, label):
    """For each locus, add up to 3 shifted windows. Counts loci toward target."""
    added_loci = 0
    added_seqs = 0
    for chrom, center in loci:
        if added_loci >= target: break
        windows_for_locus = []
        ok = True
        for off in WINDOW_OFFSETS:
            ws = center + off - L // 2
            we = ws + L
            if ws < 0 or we > contig_lens[chrom]:
                ok = False; break
            key = (chrom, ws)
            if key in seen:
                ok = False; break
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                ok = False; break
            windows_for_locus.append((key, seq))
        if not ok:
            continue
        for key, seq in windows_for_locus:
            seen.add(key)
            seqs.append(seq)
        added_loci += 1
        added_seqs += len(WINDOW_OFFSETS)
    print(f"  {label}: {added_loci}/{target} loci ({added_seqs} seqs)")
    return added_seqs


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
        loci = by_class[grp]
        rng.shuffle(loci)
        add_multiwindow(seqs, seen, fa, contig_lens, loci, target, f"cCRE {grp}")

    for cell, path in PEAK_FILES.items():
        peaks = list(parse_peaks(path))
        rng.shuffle(peaks)
        add_multiwindow(seqs, seen, fa, contig_lens, peaks, DNASE_TARGET, f"DNase {cell}")

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
        if seq is None: continue
        key = (chrom, start)
        if key in seen: continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  random: {added}/{N_RANDOM} ({tries} tries)")

    print(f"total: {len(seqs)}")
    # Pad or trim to N
    if len(seqs) > N:
        rng.shuffle(seqs)
        seqs = seqs[:N]
    elif len(seqs) < N:
        # add more random to reach N
        extra = N - len(seqs)
        added2 = 0
        tries2 = 0
        while added2 < extra and tries2 < 200_000:
            tries2 += 1
            chrom = nprng.choice(chrom_list, p=w)
            clen = contig_lens[chrom]
            start = int(nprng.integers(0, clen - L))
            seq = fetch_clean(fa, chrom, start, start + L)
            if seq is None: continue
            key = (chrom, start)
            if key in seen: continue
            seen.add(key)
            seqs.append(seq)
            added2 += 1
        print(f"  filler random: {added2}")

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
