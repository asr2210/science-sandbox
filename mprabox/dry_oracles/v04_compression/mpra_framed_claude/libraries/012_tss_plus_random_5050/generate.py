"""Experiment 012: 25k TSS-proximal + 25k uniform random.

Sharpens the test of 011. With 25k of each distribution (vs 30k+10k+10k
in 011), each component has enough samples to potentially be learned
in its own right. Tests whether the model's capacity constraint is
hard ("can only fit one distribution well") or soft ("can fit both
given enough samples").

Why this generalizes: a model that has learned BOTH the natural-DNA
distribution and the random-sequence distribution should be able to
handle a wider range of unknown test sequences for unseen cell
types. Even if the eval set is mostly natural, having seen random
calibrates the model for OOD cases.
"""
import os
import random
import numpy as np
from pathlib import Path

N_TSS = 25_000
N_RANDOM = 25_000
N_TOTAL = N_TSS + N_RANDOM
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
            p = line.rstrip("\n").split("\t")
            if len(p) < 5: continue
            if p[2] not in out: continue
            tss = int(p[4]) if p[3] == "+" else int(p[5])
            out[p[2]].add(tss)
    return {c: sorted(v) for c, v in out.items()}

def main():
    chrom_seqs = {c: load_chrom(DATA_DIR / f"{c}.fa") for c in CHROMS}
    tss_by_chrom = parse_refseq_tss(DATA_DIR / "ncbiRefSeq.txt", set(CHROMS))
    rng = np.random.default_rng(SEED)
    pyrng = random.Random(SEED + 1)

    intervals = []
    for c in CHROMS:
        chrlen = len(chrom_seqs[c])
        ivs = [(max(0, t - TSS_FLANK), min(chrlen, t + TSS_FLANK))
               for t in tss_by_chrom[c]]
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
    iv_w = iv_lens / iv_lens.sum()

    tss_seqs = []
    while len(tss_seqs) < N_TSS:
        ii = rng.choice(len(intervals), p=iv_w)
        c, s, e = intervals[ii]
        if e - s < LEN: continue
        pos = rng.integers(s, e - LEN + 1)
        cs = chrom_seqs[c]
        if pos + LEN > len(cs): continue
        w = cs[pos:pos + LEN]
        if "N" in w: continue
        if rng.random() < 0.5: w = revcomp(w)
        tss_seqs.append(w)
    print(f"TSS: {len(tss_seqs)}")

    alphabet = np.array(list("ACGT"))
    idx = rng.integers(0, 4, size=(N_RANDOM, LEN), dtype=np.int8)
    random_seqs = ["".join(row) for row in alphabet[idx]]
    print(f"Random: {len(random_seqs)}")

    seqs = tss_seqs + random_seqs
    pyrng.shuffle(seqs)
    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} to {out_path}")

if __name__ == "__main__":
    main()
