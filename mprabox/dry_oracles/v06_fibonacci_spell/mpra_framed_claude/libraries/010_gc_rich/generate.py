"""
Experiment 010: GC-rich chr22 windows.

Theory:
  009 revealed that dinucleotide composition is doing the work, not
  motifs. Now test whether shifting toward higher GC content (promoter-
  like composition) raises or lowers eval. This isolates the
  *direction* of compositional bias.

Design:
  - Scan chr22 for all valid 200bp windows.
  - Compute GC% for each window.
  - Take the top 25-30% by GC% (~55-65% GC range).
  - Sample 50k unique windows from this filtered set.
  - Random orientation.
  - Seed=42.

Generalization rationale:
  Active promoters and CpG islands are GC-rich across cell types. If
  the eval rewards GC-rich composition (proxy for "active region
  likely"), this library should outperform median-composition chr22
  random. If it underperforms, then matching the median composition
  matters more than biasing toward GC-rich. Either way, informative.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
GC_QUANTILE = 0.30  # take top 30% by GC

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

    # Sliding 200bp windows with stride 50 (to limit memory) — for GC calc
    # We sample uniformly from non-overlapping windows for diversity.
    # Use stride = 200 (non-overlapping) for the candidate pool.
    stride = 200
    candidates = []
    i = 0
    while i + SEQ_LEN <= L:
        w = chr22[i:i + SEQ_LEN]
        if all(c in ALPHABET for c in w):
            gc = (w.count("G") + w.count("C")) / SEQ_LEN
            candidates.append((gc, i))
        i += stride
    print(f"Non-overlapping valid windows: {len(candidates):,}")

    # Sort by GC, take top GC_QUANTILE
    candidates.sort(reverse=True)
    cutoff = int(len(candidates) * GC_QUANTILE)
    top = candidates[:cutoff]
    print(f"Top {GC_QUANTILE*100:.0f}% pool: {len(top):,}, GC range: "
          f"{top[-1][0]:.3f} to {top[0][0]:.3f}")

    # If pool < N_SEQS, fill from sliding windows at stride 50 within top regions
    if len(top) < N_SEQS:
        # Expand pool by adding nearby 50bp-shifted windows around top positions
        top_positions = set(pos for gc, pos in top)
        expanded = list(top)
        for gc, pos in top:
            for offset in (50, 100, 150, -50, -100, -150):
                p = pos + offset
                if 0 <= p and p + SEQ_LEN <= L:
                    w = chr22[p:p + SEQ_LEN]
                    if all(c in ALPHABET for c in w):
                        g = (w.count("G") + w.count("C")) / SEQ_LEN
                        if g >= top[-1][0]:
                            expanded.append((g, p))
        print(f"Expanded pool: {len(expanded):,}")
        top = expanded

    # Sample N_SEQS unique positions
    positions = list({pos: gc for gc, pos in top}.keys())
    print(f"Unique positions in pool: {len(positions):,}")
    if len(positions) < N_SEQS:
        # sample with replacement
        sampled = [rng.choice(positions) for _ in range(N_SEQS)]
    else:
        sampled = rng.sample(positions, N_SEQS)

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for s in sampled:
            w = chr22[s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
    # Report average GC
    gcs = []
    with open(out) as fh:
        for line in fh:
            gcs.append((line.count("G") + line.count("C")) / SEQ_LEN)
    print(f"Wrote {N_SEQS}. Mean GC = {sum(gcs)/len(gcs):.3f}, "
          f"min={min(gcs):.3f}, max={max(gcs):.3f}")

if __name__ == "__main__":
    main()
