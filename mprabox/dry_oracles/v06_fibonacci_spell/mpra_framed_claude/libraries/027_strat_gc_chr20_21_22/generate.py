"""
Experiment 027: chr20+chr21+chr22 triple-chromosome 10-bin GC strat.

024 (chr20+chr22) = NEW BEST eval_01 = 0.1376.
T22: unique natural compatible windows per bin matters.
T23: chr20 is chr22-compatible; chr19 was not.

Hypothesis: chr21 is also chr22-compatible (small chromosome, GC ~0.41,
less gene-dense than chr19). Adding chr21 → triple pool. If chr21 is
compatible, 027 > 024.

Design: chr20+chr21+chr22 stride=50, 10 quantile bins × 5k. Seed=42.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 10
PER_BIN = N_SEQS // N_BINS  # 5000

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
    chroms = {
        "chr22": load_fasta("data/chr22.fa"),
        "chr20": load_fasta("data/chr20.fa"),
        "chr21": load_fasta("data/chr21.fa"),
    }
    print(f"chr22: {len(chroms['chr22']):,} chr20: {len(chroms['chr20']):,} "
          f"chr21: {len(chroms['chr21']):,}")
    cand = (collect(chroms['chr22'], 'chr22') +
            collect(chroms['chr20'], 'chr20') +
            collect(chroms['chr21'], 'chr21'))
    print(f"Combined candidates: {len(cand):,}")
    cand.sort()
    n = len(cand)
    sampled = set()
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = cand[lo:hi]
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            counts = {"chr20": 0, "chr21": 0, "chr22": 0}
            for gc, chrom, pos in shuffled:
                k = (chrom, pos)
                if k in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(k)
                counts[chrom] += 1
                if len(chosen) >= PER_BIN: break
            print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                  f"chose {counts}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
