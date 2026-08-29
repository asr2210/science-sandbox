"""
Experiment 029: chr20-ONLY 10-bin GC strat × 5k.

Diagnostic for 024's gain. If chr20 alone ≈ 024, chr20 carries all
the signal. If chr20 alone < 013 (chr22-only), then chr22 IS uniquely
informative and 024's gain comes from COMBINING two chromosomes.

Design: chr20 stride=50, 10 quantile bins × 5k. Random orientation.
Seed=42.
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

def main():
    rng = random.Random(SEED)
    chr20 = load_fasta("data/chr20.fa")
    L = len(chr20)
    stride = 50
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr20[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            candidates.append((gc, i))
        i += stride
    print(f"chr20 candidates: {len(candidates):,}")
    candidates.sort()
    n = len(candidates)
    sampled = set()
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for b in range(N_BINS):
            lo = (b * n) // N_BINS
            hi = ((b + 1) * n) // N_BINS
            bin_pool = candidates[lo:hi]
            shuffled = bin_pool.copy()
            rng.shuffle(shuffled)
            chosen = []
            for gc, pos in shuffled:
                if pos in sampled: continue
                chosen.append((gc, pos))
                sampled.add(pos)
                if len(chosen) >= PER_BIN: break
            if b in (0, 4, 9):
                print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
                      f"chose {len(chosen)}")
            for gc, pos in chosen:
                w = chr20[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
