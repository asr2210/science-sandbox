"""
Experiment 011 — TF-diversity-curated natural windows.

Hypothesis: windows with high *combinatorial* TF binding (many unique
TFs bound, per ReMap) carry more regulatory grammar per training
example. Training on these should give the model more "syntax" per
sequence than uniformly sampled cCRE/DHS.

Design (50K):
  Bin hg38 into 200bp tiles. Each ReMap peak → tile via its summit.
  Score each tile = |unique TFs bound in that tile|. Take the top
  50K tiles by score, sample 200bp window centered at the tile
  midpoint with a small random off-center jitter.
"""

import gzip
import os
import sys
import numpy as np
from collections import defaultdict
from pyfaidx import Fasta

L = 200
SEED = 0
TILE = 200
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
REMAP = os.path.join(DATA, "remap_nr.bed.gz")

HG38_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
ALPHABET = set("ACGT")


def build_tile_diversity():
    """Stream ReMap, return dict[(chr, tile_id)] -> set(TFs)."""
    tiles = defaultdict(set)
    n = 0
    with gzip.open(REMAP, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in HG38_CHROMS:
                continue
            try:
                summit = int(parts[6])
            except (IndexError, ValueError):
                continue
            tf_cell = parts[3]
            tf = tf_cell.split(":")[0]
            tile_id = summit // TILE
            tiles[(chrom, tile_id)].add(tf)
            n += 1
            if n % 5_000_000 == 0:
                print(f"  read {n//1_000_000}M peaks, {len(tiles)} tiles",
                      file=sys.stderr)
    print(f"  total: {n} peaks, {len(tiles)} unique tiles", file=sys.stderr)
    return tiles


def main():
    rng = np.random.default_rng(SEED)
    print("Loading hg38...", file=sys.stderr)
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Building tile diversity from ReMap...", file=sys.stderr)
    tiles = build_tile_diversity()

    print("Ranking tiles by # unique TFs...", file=sys.stderr)
    items = [((c, t), len(tfs)) for (c, t), tfs in tiles.items()]
    items.sort(key=lambda x: -x[1])

    print(f"Top tile diversity: {items[0][1]}", file=sys.stderr)
    print(f"Tile #50000 diversity: {items[49999][1]}", file=sys.stderr)
    print(f"Tile #200000 diversity: {items[199999][1]}", file=sys.stderr)

    # Take top ~150K tiles (give buffer for N rejection)
    cand = items[:150_000]
    rng.shuffle(cand)

    out = []
    for (chrom, tile_id), _ in cand:
        if chrom not in fa:
            continue
        # Window centered at tile midpoint with small jitter
        center = tile_id * TILE + TILE // 2
        jitter = int(rng.integers(-50, 51))
        start = center + jitter - L // 2
        clen = len(fa[chrom])
        if start < 0 or start + L > clen:
            continue
        seq = str(fa[chrom][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        out.append(seq)
        if len(out) >= 50_000:
            break

    print(f"Total: {len(out)}", file=sys.stderr)
    assert len(out) == 50_000

    perm = rng.permutation(len(out))
    out = [out[i] for i in perm]
    with open(OUT, "w") as f:
        for s in out:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
