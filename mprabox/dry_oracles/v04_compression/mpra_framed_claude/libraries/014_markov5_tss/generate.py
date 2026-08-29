"""Experiment 014: 5th-order Markov chain on TSS-proximal DNA.

Train a 5th-order (6-mer context) Markov chain on 008's TSS-proximal
real sequences, then sample 50k synthetic 200bp sequences from it.
Preserves all 6-mer frequencies exactly but breaks all longer-range
structure (real motifs, repeats, conservation, gene architecture).

Tests how much of the natural-DNA training value is captured by
local k-mer statistics alone vs longer-range patterns.

Why this generalizes: if 5th-order Markov sampling matches or beats
008, we have an unlimited source of "natural-looking" training data
that can be sampled with any controllable mean composition, and
isn't constrained to actual human DNA — useful for cell types whose
regulatory genome differs from the training source.
"""
import random
import numpy as np
from collections import defaultdict
from pathlib import Path

N_TOTAL = 50_000
LEN = 200
ORDER = 5  # 5th-order = 6-mer context (5 prev nts -> next nt)
SEED = 42

HERE = Path(__file__).parent
SRC = HERE.parents[0] / "008_tss_proximal_random" / "sequences_0.txt"

ALPH = "ACGT"

def main():
    rng = np.random.default_rng(SEED)
    pyrng = random.Random(SEED + 1)

    # Read source sequences
    with open(SRC) as f:
        src_seqs = [l.strip() for l in f if l.strip()]
    print(f"Source sequences: {len(src_seqs)}")

    # Count (context -> next-nt) transitions across all sources
    trans = defaultdict(lambda: np.zeros(4, dtype=np.float64))
    starts = defaultdict(int)
    for s in src_seqs:
        if len(s) <= ORDER: continue
        starts[s[:ORDER]] += 1
        for i in range(len(s) - ORDER):
            ctx = s[i:i + ORDER]
            nxt = s[i + ORDER]
            j = ALPH.index(nxt)
            trans[ctx][j] += 1.0

    # Normalize to probabilities, with smoothing
    ctx_list = list(trans.keys())
    ctx_to_p = {}
    for c in ctx_list:
        counts = trans[c] + 0.1  # tiny smoothing
        ctx_to_p[c] = counts / counts.sum()

    # Build starting-kmer sampler
    starts_keys = list(starts.keys())
    starts_probs = np.array([starts[k] for k in starts_keys], dtype=np.float64)
    starts_probs /= starts_probs.sum()

    print(f"Trained on {len(ctx_list)} contexts (out of {4**ORDER} possible)")

    # Sample sequences
    alphabet = np.array(list(ALPH))
    seqs = []
    backoff_count = 0
    for n in range(N_TOTAL):
        idx0 = rng.choice(len(starts_keys), p=starts_probs)
        seq = list(starts_keys[idx0])
        for _ in range(LEN - ORDER):
            ctx = "".join(seq[-ORDER:])
            if ctx in ctx_to_p:
                p = ctx_to_p[ctx]
            else:
                # Backoff: uniform
                p = np.array([0.25, 0.25, 0.25, 0.25])
                backoff_count += 1
            j = rng.choice(4, p=p)
            seq.append(ALPH[j])
        seqs.append("".join(seq))
    print(f"Generated {len(seqs)} sequences, {backoff_count} backoffs")

    pyrng.shuffle(seqs)
    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} to {out_path}")

if __name__ == "__main__":
    main()
