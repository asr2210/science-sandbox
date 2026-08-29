"""
Experiment 016: Hybrid GC-strat + CpG-strat chr22 windows.

Theory:
  012 (GC-strat) tops eval_01 cluster (~0.137 on evals 1/2/3/5/6/11/12/14)
  014 (CpG-strat) tops eval_04/07/09 cluster (~0.137-0.139)
  Both are chr22 stratified, different axes. The per-eval winners are
  almost disjoint.

  Hypothesis: combining 25k from each captures both per-eval emphases.
  If the model can learn the union of compositional patterns from a
  hybrid library, the mean across evals should beat either alone.

Design:
  Generate the two stratified pools (5 GC bins x 5k + 5 CpG bins x 5k),
  ensuring positions are unique within each, then concatenate.
  Total = 50k. Random orientation. Seed=42.
"""

import os
import random

N_PER_HALF = 25_000
SEQ_LEN = 200
SEED = 42
N_BINS = 5

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

def cpg_count(s):
    n = 0
    for i in range(len(s) - 1):
        if s[i] == "C" and s[i+1] == "G":
            n += 1
    return n

def sample_stratified(candidates, key_fn, per_bin, rng, excluded_positions):
    """candidates: list of (pos,) where pos is offset into chr22.
    key_fn: function returning the value to stratify on for position.
    Returns list of (pos,) chosen, balanced across N_BINS quantile bins."""
    keyed = [(key_fn(pos), pos) for pos in candidates]
    keyed.sort()
    n = len(keyed)
    chosen = []
    used = set(excluded_positions)
    bin_stats = []
    for b in range(N_BINS):
        lo = (b * n) // N_BINS
        hi = ((b + 1) * n) // N_BINS
        bin_pool = keyed[lo:hi]
        rng.shuffle(bin_pool)
        bc = 0
        for k, pos in bin_pool:
            if pos in used:
                continue
            chosen.append(pos)
            used.add(pos)
            bc += 1
            if bc >= per_bin:
                break
        bin_stats.append((bin_pool[0][0], bin_pool[-1][0], bc))
    return chosen, used, bin_stats

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)
    stride = 50
    cand_positions = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            cand_positions.append(i)
        i += stride
    print(f"Candidate windows (stride=50): {len(cand_positions):,}")

    # Cache GC and CpG for all candidates once
    pos_to_gc = {}
    pos_to_cpg = {}
    for pos in cand_positions:
        w = chr22[pos:pos + SEQ_LEN]
        pos_to_gc[pos] = (w.count("G") + w.count("C")) / SEQ_LEN
        pos_to_cpg[pos] = cpg_count(w)

    per_bin = N_PER_HALF // N_BINS  # 5000

    # Half A: GC-stratified
    gc_chosen, used, gc_bins = sample_stratified(
        cand_positions, lambda p: pos_to_gc[p], per_bin, rng,
        excluded_positions=set(),
    )
    print(f"GC half: chose {len(gc_chosen)}; bins:")
    for lo, hi, c in gc_bins:
        print(f"  GC [{lo:.3f},{hi:.3f}] -> {c}")

    # Half B: CpG-stratified, excluding positions already chosen
    cpg_chosen, used2, cpg_bins = sample_stratified(
        cand_positions, lambda p: pos_to_cpg[p], per_bin, rng,
        excluded_positions=used,
    )
    print(f"CpG half: chose {len(cpg_chosen)}; bins:")
    for lo, hi, c in cpg_bins:
        print(f"  CpG [{lo},{hi}] -> {c}")

    all_positions = gc_chosen + cpg_chosen
    print(f"Combined: {len(all_positions)} (unique: {len(set(all_positions))})")

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for pos in all_positions:
            w = chr22[pos:pos + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")
    if n_written != 50_000:
        print(f"WARNING: wrote {n_written}, expected 50000")

if __name__ == "__main__":
    main()
