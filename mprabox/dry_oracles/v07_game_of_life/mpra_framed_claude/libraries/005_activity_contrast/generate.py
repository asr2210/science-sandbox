"""
Experiment 005 — explicit activity-range contrast.

Design (50K):
  20K active: cCRE PLS+pELS+dELS centered (predicted strongly active)
  20K silent: natural windows >5kb from any cCRE/DHS summit
  10K natural random (mid)

If activity-range contrast matters, we should see a real lift (>+0.005)
over the 4-way mix.
"""

import bisect
import gzip
import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

HG38 = os.path.join(DATA, "hg38.fa")
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ACTIVE_CCRE = {"PLS", "pELS", "dELS"}
SILENT_BUFFER = 5000  # at least 5kb from any cCRE or DHS summit
ALPHABET = set("ACGT")


def load_active_ccre():
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] in ACTIVE_CCRE:
                rows.append((parts[0], (int(parts[1]) + int(parts[2])) // 2))
    return rows


def load_all_anchors():
    """All chromosomal positions that should be avoided when seeking silent
    regions: all cCRE centers (low + high) plus all DHS summits."""
    anchors = {c: [] for c in HG38_CHROMS}
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c in anchors:
                mid = (int(parts[1]) + int(parts[2])) // 2
                anchors[c].append(mid)
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        chr_i = header.index("seqname")
        summit_i = header.index("summit")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[chr_i]
            if c in anchors:
                anchors[c].append(int(parts[summit_i]))
    for c in anchors:
        anchors[c].sort()
    return anchors


def sample_window(fa, c, anchor, rng, min_off=20, max_off=180):
    offset = int(rng.integers(min_off, max_off))
    start = anchor - offset
    if c not in fa:
        return None
    chrom_len = len(fa[c])
    if start < 0 or start + L > chrom_len:
        return None
    seq = str(fa[c][start:start + L]).upper()
    if len(seq) != L or not set(seq).issubset(ALPHABET):
        return None
    return seq


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    chroms = [c for c in HG38_CHROMS if c in fa]
    chrom_lens = {c: len(fa[c]) for c in chroms}
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()

    print("Loading active cCREs...", file=sys.stderr)
    active_anchors = load_active_ccre()
    print(f"  {len(active_anchors)} active cCREs", file=sys.stderr)

    print("Sampling 20K active...", file=sys.stderr)
    idxs = rng.permutation(len(active_anchors))
    active_seqs = []
    for i in idxs:
        c, mid = active_anchors[i]
        s = sample_window(fa, c, mid, rng, min_off=20, max_off=180)
        if s is None:
            continue
        active_seqs.append(s)
        if len(active_seqs) >= 20_000:
            break
    print(f"  Got {len(active_seqs)}", file=sys.stderr)

    print("Loading all regulatory anchors (cCRE + DHS)...", file=sys.stderr)
    all_anchors = load_all_anchors()
    for c in chroms:
        print(f"    {c}: {len(all_anchors[c])} anchors", file=sys.stderr)

    print("Sampling 20K silent (>5kb from any anchor)...", file=sys.stderr)
    silent_seqs = []
    attempts = 0
    while len(silent_seqs) < 20_000:
        attempts += 1
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, chrom_lens[c] - L))
        center = start + L // 2
        anchors = all_anchors[c]
        i = bisect.bisect_left(anchors, center)
        nearest = float("inf")
        if i < len(anchors):
            nearest = min(nearest, anchors[i] - center)
        if i > 0:
            nearest = min(nearest, center - anchors[i - 1])
        if nearest < SILENT_BUFFER:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        silent_seqs.append(seq)
    print(f"  Got {len(silent_seqs)} in {attempts} attempts "
          f"(accept rate {len(silent_seqs)/attempts:.3f})", file=sys.stderr)

    print("Sampling 10K random natural...", file=sys.stderr)
    nat_seqs = []
    while len(nat_seqs) < 10_000:
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        nat_seqs.append(s)

    seqs = active_seqs + silent_seqs + nat_seqs
    print(f"Total: {len(seqs)}", file=sys.stderr)
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
