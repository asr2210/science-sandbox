"""
Experiment 021 — DHS component-stratified library.

Tests if cell-type/tissue breadth in DHS helps unseen-cell-type
generalization (the real task goal).

Design (50K):
  ~3125 DHS summits per component, across 16 components (Primitive,
  Neural, Stromal A/B, Lymphoid, Placental, Musculoskeletal,
  Cancer/epithelial, Myeloid/erythroid, Organ/renal, Tissue invariant,
  Digestive, Renal/cancer, Cardiac, Pulmonary, Vascular).
  Anchored 200bp windows ±30-170bp from summit.
"""

import gzip
import os
import sys
from collections import defaultdict
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
PER_COMP = 3125  # 16 components * 3125 = 50000
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")
HG38_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
ALPHABET = set("ACGT")


def load_dhs_by_component():
    out = defaultdict(list)
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        ci = header.index("seqname")
        si = header.index("summit")
        comp_i = header.index("component")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[ci] not in HG38_CHROMS:
                continue
            out[parts[comp_i]].append((parts[ci], int(parts[si])))
    return out


def sample_anchored(fa, anchors, n, rng, min_off=30, max_off=170):
    idxs = rng.permutation(len(anchors))
    out = []
    for i in idxs:
        c, anchor = anchors[i]
        offset = int(rng.integers(min_off, max_off))
        start = anchor - offset
        clen = len(fa[c])
        if start < 0 or start + L > clen:
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
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Loading DHS by component...", file=sys.stderr)
    by_comp = load_dhs_by_component()
    print(f"  {len(by_comp)} components", file=sys.stderr)
    for k in sorted(by_comp):
        print(f"  {k}: {len(by_comp[k])}", file=sys.stderr)

    total = 0
    seqs = []
    for comp in sorted(by_comp):
        anchors = by_comp[comp]
        s = sample_anchored(fa, anchors, PER_COMP, rng)
        print(f"  {comp}: got {len(s)}", file=sys.stderr)
        seqs.extend(s)
        total += len(s)

    # Top up if any component fell short
    if total < 50_000:
        deficit = 50_000 - total
        print(f"  total deficit {deficit}, sampling more from largest", file=sys.stderr)
        largest = max(by_comp, key=lambda k: len(by_comp[k]))
        extra = sample_anchored(fa, by_comp[largest], deficit, rng)
        seqs.extend(extra)
    seqs = seqs[:50_000]
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
