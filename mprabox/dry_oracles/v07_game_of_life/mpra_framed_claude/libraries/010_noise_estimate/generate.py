"""
Experiment 002 — replicate v04 best 4-way mix.

Recipe (from v04 exp 011 which hit eval_01=0.501):
  20K natural genomic (length-weighted hg38 chr1-22,X,Y)
  15K cCRE (high-conf: PLS+pELS+dELS+CA-TF+CA-CTCF) at random off-center
  10K DHS Index summits (random sample)
   5K mouse mm39 natural windows
  Total: 50,000
"""

import gzip
import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 1
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

HG38 = os.path.join(DATA, "hg38.fa")
MM39 = os.path.join(DATA, "mm39.fa")
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}

ALPHABET = set("ACGT")


def sample_natural(fa, chroms, n, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    chroms = [c for c in chroms if c in lens]
    weights = np.array([lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        out.append(s)
    return out


def load_ccre_high_conf():
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] in HIGH_CONF_CCRE:
                rows.append((parts[0], int(parts[1]), int(parts[2])))
    return rows


def load_dhs_summits():
    summits = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            summits.append((parts[0], int(parts[6])))
    return summits


def sample_ccre_offcenter(fa, rows, n, rng):
    """Take 200bp window with cCRE midpoint at a random offset within."""
    rows = [r for r in rows if r[0] in fa]
    idxs = rng.choice(len(rows), size=min(n * 3, len(rows)), replace=False)
    out = []
    for i in idxs:
        c, s, e = rows[i]
        mid = (s + e) // 2
        offset = int(rng.integers(20, L - 20))  # mid within [20, L-20] of window
        start = mid - offset
        chrom_len = len(fa[c])
        if start < 0 or start + L > chrom_len:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        out.append(seq)
        if len(out) >= n:
            break
    return out


def sample_dhs(fa, summits, n, rng):
    summits = [s for s in summits if s[0] in fa]
    idxs = rng.choice(len(summits), size=min(n * 3, len(summits)), replace=False)
    out = []
    for i in idxs:
        c, summit = summits[i]
        offset = int(rng.integers(40, L - 40))
        start = summit - offset
        chrom_len = len(fa[c])
        if start < 0 or start + L > chrom_len:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        out.append(seq)
        if len(out) >= n:
            break
    return out


def main():
    rng = np.random.default_rng(SEED)
    hg38 = Fasta(HG38, sequence_always_upper=True)
    mm39 = Fasta(MM39, sequence_always_upper=True)

    print("Sampling natural human...", file=sys.stderr)
    nat_h = sample_natural(hg38, HG38_CHROMS, 20_000, rng)

    print("Loading cCRE high-conf...", file=sys.stderr)
    ccre = load_ccre_high_conf()
    print(f"  {len(ccre)} high-conf cCREs", file=sys.stderr)
    print("Sampling cCRE off-center...", file=sys.stderr)
    ccre_seqs = sample_ccre_offcenter(hg38, ccre, 15_000, rng)

    print("Loading DHS summits...", file=sys.stderr)
    dhs = load_dhs_summits()
    print(f"  {len(dhs)} DHS summits", file=sys.stderr)
    print("Sampling DHS windows...", file=sys.stderr)
    dhs_seqs = sample_dhs(hg38, dhs, 10_000, rng)

    print("Sampling mouse natural...", file=sys.stderr)
    nat_m = sample_natural(mm39, MM39_CHROMS, 5_000, rng)

    seqs = nat_h + ccre_seqs + dhs_seqs + nat_m
    print(f"Total: {len(seqs)}", file=sys.stderr)
    assert len(seqs) == 50_000

    # Shuffle so adjacent sequences are mixed sources
    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]

    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
