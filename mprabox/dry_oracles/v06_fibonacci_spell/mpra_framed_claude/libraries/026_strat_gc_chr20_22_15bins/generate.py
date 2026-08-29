"""
Experiment 026: chr20+chr22 15-bin GC strat (3333-ish per bin).

024 10-bin = 0.1376 (best). Test if 15-bin extracts more benefit
from the larger candidate pool. 50000 / 15 = 3333.33 → 3333 per bin
+ extra 5 distributed.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 15
BASE_PER_BIN = N_SEQS // N_BINS  # 3333

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
    # Distribute 50000 = 15*3333 + 5 → first 5 bins get 3334
    per_bin = [BASE_PER_BIN + 1 if b < 5 else BASE_PER_BIN for b in range(N_BINS)]
    assert sum(per_bin) == N_SEQS
    sampled = set()
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for b in range(N_BINS):
            need = per_bin[b]
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = cand[lo:hi]
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            for gc, chrom, pos in shuffled:
                k = (chrom, pos)
                if k in sampled: continue
                chosen.append((gc, chrom, pos))
                sampled.add(k)
                if len(chosen) >= need: break
            if b % 3 == 0 or b == N_BINS - 1:
                print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                      f"need={need}, chose={len(chosen)}")
            for gc, chrom, pos in chosen:
                w = chroms[chrom][pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out_path))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
