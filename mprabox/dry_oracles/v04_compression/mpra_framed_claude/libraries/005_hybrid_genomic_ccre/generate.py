"""Experiment 005: 50/50 hybrid of random genomic windows + cCREs.

25,000 random GRCh38 200bp windows + 25,000 cCRE-centered 200bp windows.
Same 6 chromosomes as before. Seed 42.

Hypothesis: a hybrid library combines the broad-coverage strengths of
random genomic (002) with the motif-density of cCREs (004). Tests
whether diversity-via-mixing produces a library better than either
pure source.

Why this generalizes beyond K562/HepG2/SKNSH: by combining "any DNA"
(covering all sequence types) with "known regulatory DNA" (covering
motif grammar density), the library spans the most ground in
sequence space. A model trained on it has seen both inactive
background and active regulatory grammar, so it can predict any
sequence the unseen-cell-type eval throws at it.
"""
import os
import random
from pathlib import Path

N_TOTAL = 50_000
N_GENOMIC = 25_000
N_CCRE = N_TOTAL - N_GENOMIC
LEN = 200
SEED = 42

HERE = Path(__file__).parent
DATA_DIR = HERE.parents[1] / "data"
CHROMS = ["chr1", "chr11", "chr19", "chr20", "chr21", "chr22"]

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
    chrom_set = set(CHROMS)
    rng = random.Random(SEED)

    # --- Part A: random genomic windows ---
    weights = [len(chrom_seqs[c]) for c in CHROMS]
    total = sum(weights)
    cum = []
    s = 0
    for w in weights:
        s += w / total
        cum.append(s)
    def pick_chrom():
        r = rng.random()
        for i, c in enumerate(cum):
            if r < c:
                return CHROMS[i]
        return CHROMS[-1]

    genomic_seqs = []
    while len(genomic_seqs) < N_GENOMIC:
        c = pick_chrom()
        cs = chrom_seqs[c]
        pos = rng.randrange(0, len(cs) - LEN)
        w = cs[pos:pos + LEN]
        if "N" in w:
            continue
        if rng.random() < 0.5:
            w = revcomp(w)
        genomic_seqs.append(w)
    print(f"Genomic: {len(genomic_seqs)}")

    # --- Part B: cCREs ---
    ccres = []
    with open(DATA_DIR / "ccres.bed") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in chrom_set:
                continue
            ccres.append((parts[0], int(parts[1]), int(parts[2])))
    rng.shuffle(ccres)
    ccre_seqs = []
    for chrom, start, end in ccres:
        if len(ccre_seqs) >= N_CCRE:
            break
        mid = (start + end) // 2
        w_start = mid - LEN // 2
        w_end = w_start + LEN
        cs = chrom_seqs[chrom]
        if w_start < 0 or w_end > len(cs):
            continue
        w = cs[w_start:w_end]
        if "N" in w:
            continue
        if rng.random() < 0.5:
            w = revcomp(w)
        ccre_seqs.append(w)
    print(f"cCREs: {len(ccre_seqs)}")

    seqs = genomic_seqs + ccre_seqs
    assert len(seqs) == N_TOTAL
    rng.shuffle(seqs)

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} sequences to {out_path}")

if __name__ == "__main__":
    main()
