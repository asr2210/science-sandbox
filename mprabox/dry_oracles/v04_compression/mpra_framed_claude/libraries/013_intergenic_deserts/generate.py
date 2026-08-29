"""Experiment 013: intergenic deserts (anti-TSS).

50k random 200bp windows from regions >25kb from ANY RefSeq TSS.
Disjoint complement of 008. Single-source, natural human DNA.

Tests where the natural-DNA training lift actually comes from:
- 013 ≈ 002 (~0.50): DNA-ness is the source; gene proximity not needed
- 013 < 002 (~0.40-0.45): gene-rich regions carry the signal
- 013 > 002: unlikely; pure intergenic is better

Why this generalizes: future cell types may be measured at
enhancers in intergenic deserts. Knowing intergenic samples are
informative tells us we can train on regions complementary to
known genes — important when the test cell type's regulatory
landscape is unknown.
"""
import os
import random
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
LEN = 200
SEED = 42
TSS_FLANK = 25_000  # excluded region around each TSS

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

    # Build excluded intervals (TSS ± 25kb merged), then complement
    desert_intervals = []
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
        # Complement on [0, chrlen)
        prev = 0
        for s, e in merged:
            if s > prev:
                desert_intervals.append((c, prev, s))
            prev = e
        if prev < chrlen:
            desert_intervals.append((c, prev, chrlen))

    total_desert = sum(e - s for _, s, e in desert_intervals)
    print(f"Deserts: {len(desert_intervals)} intervals, {total_desert/1e6:.1f} Mb")

    iv_lens = np.array([e - s for _, s, e in desert_intervals], dtype=np.float64)
    iv_w = iv_lens / iv_lens.sum()

    seqs = []
    tries = 0
    while len(seqs) < N_TOTAL:
        tries += 1
        ii = rng.choice(len(desert_intervals), p=iv_w)
        c, s, e = desert_intervals[ii]
        if e - s < LEN: continue
        pos = rng.integers(s, e - LEN + 1)
        cs = chrom_seqs[c]
        if pos + LEN > len(cs): continue
        w = cs[pos:pos + LEN]
        if "N" in w: continue
        if rng.random() < 0.5: w = revcomp(w)
        seqs.append(w)
    print(f"Generated {len(seqs)} from {tries} tries")

    pyrng.shuffle(seqs)
    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} to {out_path}")

if __name__ == "__main__":
    main()
