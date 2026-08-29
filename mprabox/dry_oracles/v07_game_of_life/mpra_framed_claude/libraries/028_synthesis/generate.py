"""
Experiment 028 — synthesis library combining all positive learnings.

T8: GC stratification is the dominant lever (+0.021).
T10: source identity fungible at the ceiling; mixing adds breadth.
T4: multi-genome doesn't hurt; mouse equally informative.

Design (50K): 5 GC bins × 10K each; within each bin, 4 sources × 2500:
  2500 hg38 natural (GC-binned)
  2500 mm39 natural (GC-binned)
  2500 hg38 DHS-anchored (GC-binned)
  2500 hg38 cCRE-anchored (GC-binned)

Best-of-all. If exceeds 0.3961 (exp 010 record): synthesis wins.
If matches: ceiling is hard at 0.395 ± 0.002 regardless of design
within the "balanced composition" tier.
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
MM39 = os.path.join(DATA, "mm39.fa")
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
ALPHABET = set("ACGT")
BINS = [(0.0, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 1.0)]
PER_SOURCE_PER_BIN = 2500


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= g < hi:
            return i
    return len(BINS) - 1


def sample_natural_gc(fa, chroms, per_bin, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()
    bins = [[] for _ in BINS]
    n = 0
    while sum(len(b) for b in bins) < sum(per_bin):
        n += 1
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        b = bin_for(gc(s))
        if len(bins[b]) < per_bin[b]:
            bins[b].append(s)
    return [s for b in bins for s in b], n


def load_ccre_class(classes):
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] in classes:
                rows.append((parts[0], (int(parts[1]) + int(parts[2])) // 2))
    return rows


def load_dhs_summits():
    out = []
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        ci = header.index("seqname")
        si = header.index("summit")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            out.append((parts[ci], int(parts[si])))
    return out


def sample_anchored_gc(fa, anchors, per_bin, rng, min_off=30, max_off=170):
    anchors = [(c, a) for c, a in anchors if c in fa]
    idxs = rng.permutation(len(anchors))
    bins = [[] for _ in BINS]
    needed = sum(per_bin)
    for i in idxs:
        if sum(len(b) for b in bins) >= needed:
            break
        c, anchor = anchors[i]
        offset = int(rng.integers(min_off, max_off))
        start = anchor - offset
        clen = len(fa[c])
        if start < 0 or start + L > clen:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        b = bin_for(gc(seq))
        if len(bins[b]) < per_bin[b]:
            bins[b].append(seq)
    return [s for b in bins for s in b], [len(b) for b in bins]


def main():
    rng = np.random.default_rng(SEED)
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)

    pb = [PER_SOURCE_PER_BIN] * 5  # 2500 per bin per source

    print("Human natural GC-strat (2500/bin)...", file=sys.stderr)
    h_nat, n1 = sample_natural_gc(hg, HG38_CHROMS, pb, rng)
    print(f"  got {len(h_nat)} after {n1} tries", file=sys.stderr)

    print("Mouse natural GC-strat (2500/bin)...", file=sys.stderr)
    m_nat, n2 = sample_natural_gc(mm, MM39_CHROMS, pb, rng)
    print(f"  got {len(m_nat)} after {n2} tries", file=sys.stderr)

    print("Loading cCRE...", file=sys.stderr)
    ccre = load_ccre_class(HIGH_CONF_CCRE)
    print("cCRE GC-strat (2500/bin)...", file=sys.stderr)
    c_seq, c_sizes = sample_anchored_gc(hg, ccre, pb, rng)
    print(f"  got {len(c_seq)}, sizes {c_sizes}", file=sys.stderr)
    if len(c_seq) < sum(pb):
        deficit = sum(pb) - len(c_seq)
        print(f"  cCRE deficit {deficit}, topping with human natural",
              file=sys.stderr)
        extra, _ = sample_natural_gc(hg, HG38_CHROMS,
                                      [(deficit // 5) + 1] * 5, rng)
        c_seq += extra[:deficit]

    print("Loading DHS...", file=sys.stderr)
    dhs = load_dhs_summits()
    print("DHS GC-strat (2500/bin)...", file=sys.stderr)
    d_seq, d_sizes = sample_anchored_gc(hg, dhs, pb, rng)
    print(f"  got {len(d_seq)}, sizes {d_sizes}", file=sys.stderr)
    if len(d_seq) < sum(pb):
        deficit = sum(pb) - len(d_seq)
        print(f"  DHS deficit {deficit}, topping with human natural",
              file=sys.stderr)
        extra, _ = sample_natural_gc(hg, HG38_CHROMS,
                                      [(deficit // 5) + 1] * 5, rng)
        d_seq += extra[:deficit]

    seqs = h_nat + m_nat + c_seq + d_seq
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
