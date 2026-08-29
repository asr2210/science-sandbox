"""
Experiment 021: Sequence-complexity stratified chr22 windows.

Theory:
  GC stratification has saturated at eval_01 ~0.137. Complexity
  (distinct trimer count, a Shannon-entropy proxy) is a different
  compositional axis:
  - Low complexity: homopolymer runs, simple repeats (AT-repeats,
    short tandem repeats). These dominate the AT-rich tail and may
    add little signal.
  - High complexity: diverse k-mer use, "informative" windows.

  Hypothesis: stratifying by complexity captures a different aspect
  of the eval distribution than GC. If 021 lifts eval_01 above 0.1375
  → complexity is a useful new axis. If 021 < 0.137 → complexity
  correlates with GC and adds nothing.

Design:
  chr22 stride=50 candidate windows. For each compute distinct trimer
  count (max 4^3 = 64 possible, max-distinct in 200bp ≈ 64). Sort and
  bin into 5 quantile bins, 10k per bin. Random orientation. Seed=42.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 5
PER_BIN = N_SEQS // N_BINS  # 10000

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

def distinct_trimers(s):
    return len({s[i:i+3] for i in range(len(s) - 2)})

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)
    stride = 50
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            comp = distinct_trimers(w)
            candidates.append((comp, i))
        i += stride
    print(f"Candidate windows: {len(candidates):,}")
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
            for comp, pos in shuffled:
                if pos in sampled:
                    continue
                chosen.append((comp, pos))
                sampled.add(pos)
                if len(chosen) >= PER_BIN:
                    break
            # GC stats for this bin
            gcs = []
            for comp, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                gcs.append((w.count("G") + w.count("C")) / SEQ_LEN)
            mean_gc = sum(gcs) / len(gcs)
            print(f"Bin {b}: trimers {bin_pool[0][0]}-{bin_pool[-1][0]}, "
                  f"pool={len(bin_pool):,}, chose={len(chosen)}, "
                  f"mean GC={mean_gc:.3f}")
            for comp, pos in chosen:
                w = chr22[pos:pos + SEQ_LEN]
                if rng.random() < 0.5:
                    w = revcomp(w)
                f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
