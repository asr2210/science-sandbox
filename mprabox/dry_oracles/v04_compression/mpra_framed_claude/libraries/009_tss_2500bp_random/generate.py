"""Experiment 009: random 200bp windows within +/-2.5kb of any RefSeq TSS.

Tightens TSS focus from 008 (±25kb) toward promoter zone. Tests the
gradient of "transcriptional bias" between broad genomic (002), TSS-
proximal (008), and tight promoter zone (009 — this).
"""
import os
import numpy as np
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42
TSS_FLANK = 2_500

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
            if len(parts) < 5:
                continue
            chrom = parts[2]
            strand = parts[3]
            tx_start = int(parts[4])
            tx_end = int(parts[5])
            if chrom not in out:
                continue
            tss = tx_start if strand == "+" else tx_end
            out[chrom].add(tss)
    return {c: sorted(v) for c, v in out.items()}

def main():
    chrom_seqs = {c: load_chrom(DATA_DIR / f"{c}.fa") for c in CHROMS}
    tss_by_chrom = parse_refseq_tss(DATA_DIR / "ncbiRefSeq.txt", set(CHROMS))
    rng = np.random.default_rng(SEED)

    intervals_by_chrom = {}
    total_intervals_bp = 0
    for c in CHROMS:
        ivs = []
        chrlen = len(chrom_seqs[c])
        for tss in tss_by_chrom[c]:
            s = max(0, tss - TSS_FLANK)
            e = min(chrlen, tss + TSS_FLANK)
            ivs.append((s, e))
        ivs.sort()
        merged = []
        for s, e in ivs:
            if merged and s <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
            else:
                merged.append((s, e))
        intervals_by_chrom[c] = merged
        total_intervals_bp += sum(e - s for s, e in merged)
    print(f"Total TSS-proximal bp (±{TSS_FLANK}): {total_intervals_bp:,}")

    flat = []
    for c in CHROMS:
        for s, e in intervals_by_chrom[c]:
            flat.append((c, s, e))
    iv_lens = np.array([e - s for _, s, e in flat], dtype=np.float64)
    iv_weights = iv_lens / iv_lens.sum()

    seqs = []
    attempts = 0
    while len(seqs) < N_SEQ:
        ii = rng.choice(len(flat), p=iv_weights)
        c, s, e = flat[ii]
        if e - s < LEN:
            continue
        pos = rng.integers(s, e - LEN + 1)
        cs = chrom_seqs[c]
        if pos + LEN > len(cs):
            continue
        window = cs[pos:pos + LEN]
        attempts += 1
        if "N" in window:
            continue
        if rng.random() < 0.5:
            window = revcomp(window)
        seqs.append(window)

    print(f"{len(seqs)} sequences from {attempts} attempts "
          f"({100 * len(seqs) / attempts:.1f}% accept)")
    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")

if __name__ == "__main__":
    main()
