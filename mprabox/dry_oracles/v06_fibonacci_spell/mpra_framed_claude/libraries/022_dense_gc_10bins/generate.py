"""
Experiment 022: Dense stride=10 chr22 sampling + 10-bin GC strat.

Theory:
  013 (stride=50, 10 GC bins × 5k) = 0.1375 eval_01 best.
  Stride=50 gives 78k candidates per bin. Maybe denser pool with
  per-bin diversity selection gives marginally better samples.

  Hypothesis: stride=10 gives ~4x more candidates per bin (312k each).
  Random sampling 5k from a larger, more compositionally-varied pool
  may reduce per-bin variance and improve generalization.

Design:
  chr22 stride=10 sliding windows → ~3.9M candidates.
  Position-dedup at ≥50bp distance to avoid near-duplicates.
  Sort by GC, 10 quantile bins, 5k per bin (random pick within bin).
  Random orientation. Seed=42.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_BINS = 10
PER_BIN = N_SEQS // N_BINS  # 5000
MIN_POS_DIST = 50

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
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)
    stride = 10
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            candidates.append((gc, i))
        i += stride
    print(f"Candidate windows (stride=10): {len(candidates):,}")
    candidates.sort()
    n = len(candidates)
    chosen_positions = []
    used = []  # sorted positions for dedup check (simple list is fine if we
               # keep used sorted and bin-by-bin add)
    for b in range(N_BINS):
        lo = (b * n) // N_BINS
        hi = ((b + 1) * n) // N_BINS
        bin_pool = candidates[lo:hi]
        shuffled = bin_pool.copy()
        rng.shuffle(shuffled)
        chosen = []
        used_set = set(used)
        for gc, pos in shuffled:
            # check distance to nearest already-chosen (across all bins)
            ok = True
            # simple: check 5 closest positions in used_set (use modulo)
            for d in range(-MIN_POS_DIST + 1, MIN_POS_DIST):
                if d == 0: continue
                if (pos + d) in used_set:
                    ok = False
                    break
            if not ok:
                continue
            chosen.append(pos)
            used_set.add(pos)
            if len(chosen) >= PER_BIN:
                break
        used.extend(chosen)
        used = list(set(used))
        print(f"Bin {b}: GC {bin_pool[0][0]:.3f}-{bin_pool[-1][0]:.3f}, "
              f"pool={len(bin_pool):,}, chose={len(chosen)}")
        chosen_positions.extend(chosen)
    print(f"Total chosen: {len(chosen_positions)}")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for pos in chosen_positions:
            w = chr22[pos:pos + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")

if __name__ == "__main__":
    main()
