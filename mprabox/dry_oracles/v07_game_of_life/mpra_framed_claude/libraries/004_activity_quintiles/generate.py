"""
Experiment 004 — activity-range engineering via DHS quintile stratification.

Hypothesis: explicit coverage of the activity range (from low to high
mean_signal) helps the model learn the discrimination boundary. T2
(library = scalar multiplier) predicts no improvement over exp 002.
Activity-range hypothesis predicts modest improvement.

Design (50K, all from DHS Index human chr1-22,X,Y):
  10K from each of 5 mean_signal quintiles
  Window: 200bp anchored at DHS summit, random offset [40, 160]
"""

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
DHS = os.path.join(DATA, "dhs_index.tsv.gz")
HG38_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
ALPHABET = set("ACGT")


def load_dhs_with_signal():
    out = []
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        chr_idx = header.index("seqname")
        summit_idx = header.index("summit")
        sig_idx = header.index("mean_signal")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[chr_idx]
            if c not in HG38_CHROMS:
                continue
            out.append((c, int(parts[summit_idx]), float(parts[sig_idx])))
    return out


def sample_window(fa, c, anchor, rng):
    offset = int(rng.integers(40, L - 40))
    start = anchor - offset
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

    print("Loading DHS Index with mean_signal...", file=sys.stderr)
    summits = load_dhs_with_signal()
    print(f"  {len(summits)} summits on primary chroms", file=sys.stderr)

    sigs = np.array([s[2] for s in summits])
    quintiles = np.quantile(sigs, [0.2, 0.4, 0.6, 0.8])
    print(f"  Quintile boundaries: {quintiles}", file=sys.stderr)

    # Bucket indices by quintile
    bucket = np.digitize(sigs, quintiles)  # 0..4
    buckets = [np.where(bucket == k)[0] for k in range(5)]
    for k, b in enumerate(buckets):
        print(f"  Bucket {k}: {len(b)} summits, "
              f"mean_signal range [{sigs[b].min():.3f}, {sigs[b].max():.3f}]",
              file=sys.stderr)

    seqs = []
    per_bucket = 10_000
    for k in range(5):
        candidates = rng.permutation(buckets[k])
        count = 0
        for idx in candidates:
            c, summit, _ = summits[idx]
            s = sample_window(fa, c, summit, rng)
            if s is None:
                continue
            seqs.append(s)
            count += 1
            if count >= per_bucket:
                break
        print(f"  Bucket {k}: sampled {count}", file=sys.stderr)

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
