"""
Experiment 028: chr20+chr22 10-bin × (2,500 chr22 + 2,500 chr20) per bin.

024 (chr20+chr22 10-bin × 5k random) = NEW BEST eval_01 0.1376.
That design had chr22:chr20 ratio varying 1396:3604 (bin 0) to
2805:2195 (bin 9). Maybe chr22 was under-represented in low-GC bins.

028 forces equal chr22+chr20 contribution per bin. Tests if guaranteed
chr22 representation in every bin (incl. low/mid-GC where chr22 is
naturally scarce in the combined pool) lifts above 0.1376.

Design: 10 quantile bins of combined chr20+chr22 candidates. Per bin:
2,500 chr22 + 2,500 chr20 (randomly chosen). Total = 50k.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 10
PER_CHROM_PER_BIN = 2500  # 2500 chr22 + 2500 chr20 per bin

ALPHABET = set("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip().upper())
    return "".join(parts)

def collect(seq, label, stride=50):
    L = len(seq); out = []; i = 0
    while i + SEQ_LEN <= L:
        w = seq[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            out.append((gc, label, i))
        i += stride
    return out

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    chr20 = load_fasta("data/chr20.fa")
    chroms = {"chr22": chr22, "chr20": chr20}
    cand = collect(chr22, "chr22") + collect(chr20, "chr20")
    cand.sort()
    n = len(cand)
    print(f"Combined candidates: {n:,}")
    sampled = set()
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = cand[lo:hi]
            # Split by chromosome
            chr22_in_bin = [(gc, "chr22", pos) for gc, c, pos in bin_pool if c == "chr22"]
            chr20_in_bin = [(gc, "chr20", pos) for gc, c, pos in bin_pool if c == "chr20"]
            # Shuffle each
            rng.shuffle(chr22_in_bin); rng.shuffle(chr20_in_bin)
            chosen = []
            for (gc, chrom, pos), label in [(x, "chr22") for x in chr22_in_bin]:
                if pos in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(pos)
                if sum(1 for _, c, _ in chosen if c == "chr22") >= PER_CHROM_PER_BIN:
                    break
            for (gc, chrom, pos), label in [(x, "chr20") for x in chr20_in_bin]:
                if pos in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(pos)
                if sum(1 for _, c, _ in chosen if c == "chr20") >= PER_CHROM_PER_BIN:
                    break
            c22 = sum(1 for _, c, _ in chosen if c == "chr22")
            c20 = sum(1 for _, c, _ in chosen if c == "chr20")
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"avail chr22={len(chr22_in_bin)}, chose chr22={c22}/chr20={c20}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
