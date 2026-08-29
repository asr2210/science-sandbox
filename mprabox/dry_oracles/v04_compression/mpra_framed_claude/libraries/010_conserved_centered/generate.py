"""Experiment 010: 200bp windows centered on phastCons conserved elements.

Sample 50k conserved-element midpoints (phastCons100way, GRCh38), filter
to autosomes, take a 200bp window centered on each. Conserved elements
are mostly 5-50bp (functional cores). Surrounding 200bp window is
natural genomic context with a likely-functional center.

Hypothesis: evolutionarily conserved sequences are enriched for
function across species/tissues. If the eval contains many conserved
regulatory elements, this library should help. Conservation is by
construction not specific to any cell type — selection acts on
function used in *some* tissue/condition.

Why this generalizes: conservation = retained function across mammals.
The retained function uses TF motifs that are shared across cell
types. A model trained here learns functionally-relevant grammar
that should transfer to any cell type that uses any subset of
mammalian regulatory machinery.
"""
import os
import random
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42

HERE = Path(__file__).parent
DATA_DIR = HERE.parents[1] / "data"
CHROMS = [f"chr{i}" for i in range(1, 23)]
CHROM_SET = set(CHROMS)

def load_chrom(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip())
    return "".join(parts).upper()

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def main():
    chrom_seqs = {c: load_chrom(DATA_DIR / f"{c}.fa") for c in CHROMS}
    rng = random.Random(SEED)

    # Load conserved elements; filter to autosomes; keep midpoint
    elements = []
    with open(DATA_DIR / "phastConsElements100way.txt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[1]
            if chrom not in CHROM_SET:
                continue
            s = int(parts[2])
            e = int(parts[3])
            # Use midpoint as the center of the 200bp window
            mid = (s + e) // 2
            elements.append((chrom, mid))
    print(f"Loaded {len(elements):,} conserved elements on autosomes")

    rng.shuffle(elements)
    seqs = []
    for chrom, mid in elements:
        if len(seqs) >= N_SEQ:
            break
        cs = chrom_seqs[chrom]
        w_start = mid - LEN // 2
        w_end = w_start + LEN
        if w_start < 0 or w_end > len(cs):
            continue
        w = cs[w_start:w_end]
        if "N" in w:
            continue
        if rng.random() < 0.5:
            w = revcomp(w)
        seqs.append(w)
    print(f"Wrote {len(seqs)} sequences")
    assert len(seqs) == N_SEQ

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")

if __name__ == "__main__":
    main()
