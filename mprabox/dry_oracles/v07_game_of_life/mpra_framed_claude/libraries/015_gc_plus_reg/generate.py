"""
Experiment 015 — GC-stratified natural + GC-stratified regulatory.

Tests orthogonality of T8 (GC) and "regulatory content" theories.
If GC is the whole story, no further lift beyond exp 014. If reg
content adds orthogonal information on top of GC balance, lift to
0.397-0.40.

Design (50K):
  25K natural windows, 5K per GC bin (≤35,35-45,45-55,55-65,>65)
  15K cCRE high-conf off-center, 3K per GC bin
  10K DHS summits, 2K per GC bin
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
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
ALPHABET = set("ACGT")
BINS = [(0.0, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 1.0)]


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= g < hi:
            return i
    return len(BINS) - 1


def sample_natural_gc(fa, chroms, per_bin, rng, max_tries=2_000_000):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()
    bins = [[] for _ in BINS]
    needed = sum(per_bin)
    n = 0
    while sum(len(b) for b in bins) < needed and n < max_tries:
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
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Natural GC-stratified 25K (5K/bin)...", file=sys.stderr)
    nat, tries = sample_natural_gc(fa, HG38_CHROMS, [5000] * 5, rng)
    print(f"  got {len(nat)} after {tries} tries", file=sys.stderr)

    print("Loading cCRE...", file=sys.stderr)
    ccre = load_ccre_class(HIGH_CONF_CCRE)
    print("cCRE GC-stratified 15K (3K/bin)...", file=sys.stderr)
    cseqs, sizes = sample_anchored_gc(fa, ccre, [3000] * 5, rng)
    print(f"  got {len(cseqs)}, bins: {sizes}", file=sys.stderr)

    # If under target due to anchor scarcity in low-GC, top up with natural
    if len(cseqs) < 15000:
        deficit = 15000 - len(cseqs)
        print(f"  cCRE deficit {deficit}, topping with natural", file=sys.stderr)
        extra, _ = sample_natural_gc(fa, HG38_CHROMS,
                                      [(deficit // 5) + 1] * 5, rng)
        cseqs += extra[:deficit]

    print("Loading DHS...", file=sys.stderr)
    dhs = load_dhs_summits()
    print("DHS GC-stratified 10K (2K/bin)...", file=sys.stderr)
    dseqs, sizes = sample_anchored_gc(fa, dhs, [2000] * 5, rng)
    print(f"  got {len(dseqs)}, bins: {sizes}", file=sys.stderr)

    if len(dseqs) < 10000:
        deficit = 10000 - len(dseqs)
        print(f"  DHS deficit {deficit}, topping with natural", file=sys.stderr)
        extra, _ = sample_natural_gc(fa, HG38_CHROMS,
                                      [(deficit // 5) + 1] * 5, rng)
        dseqs += extra[:deficit]

    seqs = nat + cseqs + dseqs
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
