"""Experiment 011: multi-source blend.

50k total: 30k TSS-proximal (±25kb), 10k broad genomic (all 22 autosomes),
10k uniform random ACGT.

Rationale: per-experiment review showed that different evals reward
different library distributions. Pure random wins eval_08 (0.110 vs
~0.09 for any genomic). TSS-proximal wins evals 01-07. Broad genomic
wins evals 10/13. A blended library should cover the union of these
distributions.

Why this generalizes: a model trained on this mixture has seen broad
natural human DNA (gene-proximal + intergenic), plus random uniform
that calibrates it for the long tail of unusual sequences. For
unknown future test distributions (different cell types, synthetic
constructs, etc.), the mixture is the safest bet.
"""
import os
import random
import numpy as np
from pathlib import Path

N_TSS = 30_000
N_GENOMIC = 10_000
N_RANDOM = 10_000
N_TOTAL = N_TSS + N_GENOMIC + N_RANDOM
LEN = 200
SEED = 42
TSS_FLANK = 25_000

HERE = Path(__file__).parent
DATA_DIR = HERE.parents[1] / "data"
CHROMS = [f"chr{i}" for i in range(1, 23)]

def load_chrom(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip())
    return "".join(parts).upper()

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def parse_refseq_tss(path, chrom_set):
    out = {c: set() for c in chrom_set}
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5: continue
            chrom = parts[2]; strand = parts[3]
            ts = int(parts[4]); te = int(parts[5])
            if chrom not in out: continue
            out[chrom].add(ts if strand == "+" else te)
    return {c: sorted(v) for c, v in out.items()}

def main():
    chrom_seqs = {c: load_chrom(DATA_DIR / f"{c}.fa") for c in CHROMS}
    tss_by_chrom = parse_refseq_tss(DATA_DIR / "ncbiRefSeq.txt", set(CHROMS))
    rng = np.random.default_rng(SEED)
    pyrng = random.Random(SEED + 1)

    # --- Part A: TSS-proximal (30k) ---
    intervals = []
    for c in CHROMS:
        chrlen = len(chrom_seqs[c])
        ivs = [(max(0, tss - TSS_FLANK), min(chrlen, tss + TSS_FLANK))
               for tss in tss_by_chrom[c]]
        ivs.sort()
        merged = []
        for s, e in ivs:
            if merged and s <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
            else:
                merged.append((s, e))
        for s, e in merged:
            intervals.append((c, s, e))
    iv_lens = np.array([e - s for _, s, e in intervals], dtype=np.float64)
    iv_weights = iv_lens / iv_lens.sum()
    tss_seqs = []
    while len(tss_seqs) < N_TSS:
        ii = rng.choice(len(intervals), p=iv_weights)
        c, s, e = intervals[ii]
        if e - s < LEN: continue
        pos = rng.integers(s, e - LEN + 1)
        cs = chrom_seqs[c]
        if pos + LEN > len(cs): continue
        w = cs[pos:pos + LEN]
        if "N" in w: continue
        if rng.random() < 0.5: w = revcomp(w)
        tss_seqs.append(w)
    print(f"TSS-proximal: {len(tss_seqs)}")

    # --- Part B: broad genomic (10k) ---
    chrom_weights = np.array([len(chrom_seqs[c]) for c in CHROMS], dtype=np.float64)
    chrom_weights /= chrom_weights.sum()
    genomic_seqs = []
    while len(genomic_seqs) < N_GENOMIC:
        ci = rng.choice(len(CHROMS), p=chrom_weights)
        cs = chrom_seqs[CHROMS[ci]]
        pos = rng.integers(0, len(cs) - LEN)
        w = cs[pos:pos + LEN]
        if "N" in w: continue
        if rng.random() < 0.5: w = revcomp(w)
        genomic_seqs.append(w)
    print(f"Broad genomic: {len(genomic_seqs)}")

    # --- Part C: uniform random (10k) ---
    alphabet = np.array(list("ACGT"))
    idx = rng.integers(0, 4, size=(N_RANDOM, LEN), dtype=np.int8)
    random_seqs = ["".join(row) for row in alphabet[idx]]
    print(f"Uniform random: {len(random_seqs)}")

    seqs = tss_seqs + genomic_seqs + random_seqs
    assert len(seqs) == N_TOTAL
    pyrng.shuffle(seqs)

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} to {out_path}")

if __name__ == "__main__":
    main()
