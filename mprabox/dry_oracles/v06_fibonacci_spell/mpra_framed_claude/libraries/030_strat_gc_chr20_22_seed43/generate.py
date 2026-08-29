"""
Experiment 030: 024's recipe (chr20+chr22 10-bin × 5k) with seed=43.

024 set a new best at eval_01 = 0.1376 (seed=42).
This is a robustness check: does a different seed give a similar
score? If yes, 024's design is stable. If no, the gain was lucky.

Design identical to 024 except SEED=43.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 43  # different from 024's seed=42
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
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            c22 = c20 = 0
            for gc, chrom, pos in shuffled:
                k = (chrom, pos)
                if k in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(k)
                if chrom == "chr22": c22 += 1
                else: c20 += 1
                if len(chosen) >= PER_BIN: break
            if b in (0, 4, 9):
                print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                      f"chose chr22:{c22}/chr20:{c20}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
