"""
Experiment 007: Saturation mutagenesis library.

Theory:
  Random-genomic plateaus at ~0.134 across 003/005/006. Hypothesis H1:
  the missing signal is gradient information — base-level effects of
  perturbations. Saturation mutagenesis (variant series around seed
  sequences) gives the model rich Δactivity-per-Δbase signal.

Design:
  - 2500 seed sequences. Each seed = a random chr22 200bp window with 3
    random TF motifs embedded at random positions and orientations.
  - For each seed: 1 original + 19 variants = 20 total.
  - Each variant: single random base substitution at a random position
    (1 of 200 positions, change to one of the 3 non-original bases).
  - Total: 2500 × 20 = 50,000.
  - Seed=42.

Generalization rationale:
  Base-resolution mutagenesis trains the model on the local sensitivity
  function: how much does activity change when a specific base flips?
  This function is rooted in TF binding biochemistry (PWM-like effects)
  and is conserved across cell types — the same base change destroys
  the same motif anywhere. A model that learns this gradient is more
  transferable than one that only learns "active vs inactive" labels
  on whole sequences.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
N_SEEDS = 2500
N_VARS_PER_SEED = 20  # includes the original
N_MOTIFS_PER_SEED = 3

MOTIFS = [
    "CACGTG", "CAGCTG", "CATCTG", "TGACTCA", "TGAGTCA", "TGACGTCA",
    "AGATAA", "TGATAA", "CCGGAAGT", "ACCGGAAGT", "TGTTTAC", "GTAAACA",
    "GGGAATTTCC", "GGGGCGGGGC", "CACCC", "CTATAAATAG", "GTTAATCATTAAC",
    "AGGTCAAAGGTCA", "ATTGCGCAAT", "TTCAGCACCATGGACAG", "TAATCC",
    "ATGCAAAT", "GGAAA", "TTCCCGGAA", "AAAGTGAAAGT", "GGACATGTCC",
    "TGTGGT", "AACAAAG", "CTTTGTT", "AACTGAC", "CCAATCA",
    "CCGCGGGGGGCAG", "CCATCTT", "CCATATATGG", "TATAAAA",
    "AGTCTAGAC", "GGAATGTG", "CAGGTA", "AGGTCA", "AGGTCATGACCT",
    "AGAACAGTGACCT", "GAATTCTAGAA", "TTTCGCGC", "GCGCATGCGC",
    "TGCTGAGTCAT", "TTCCTAGAA", "GTCATGAT", "AGCTGCT", "AGGTGT",
    "ATCAATCA", "CTAGTCCT", "GGAAGTGA", "TGACAGGT", "AGGGTGTGGTCA",
    "CACCCT", "TTTCACTTTCC", "ATGACTCAGCA", "CCCGCCCCC", "TGACCTTG",
    "GCTAATTGG",
]

ALPHABET = set("ACGT")
ALPHA_LIST = list("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip().upper())
    return "".join(parts)

def insert_motifs(rng, chars, n):
    L = len(chars)
    used = []
    for _ in range(n):
        m = rng.choice(MOTIFS)
        if rng.random() < 0.5:
            m = revcomp(m)
        ml = len(m)
        for attempt in range(20):
            pos = rng.randrange(0, L - ml + 1)
            ok = all(pos + ml <= s or pos >= e for s, e in used)
            if ok:
                chars[pos:pos + ml] = list(m)
                used.append((pos, pos + ml))
                break
    return chars

def make_variant(rng, chars):
    """Single random base substitution at random position."""
    v = list(chars)
    pos = rng.randrange(len(v))
    orig = v[pos]
    choices = [b for b in ALPHA_LIST if b != orig]
    v[pos] = rng.choice(choices)
    return "".join(v)

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    # valid starts
    L = len(chr22)
    starts = []
    i = 0
    while i < L:
        if chr22[i] in ALPHABET:
            j = i
            while j < L and chr22[j] in ALPHABET:
                j += 1
            if j - i >= SEQ_LEN:
                starts.extend(range(i, j - SEQ_LEN + 1))
            i = j
        else:
            i += 1
    seed_starts = rng.sample(starts, N_SEEDS)

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    written = 0
    with open(out, "w") as f:
        for s in seed_starts:
            chars = list(chr22[s:s + SEQ_LEN])
            if rng.random() < 0.5:
                chars = list(revcomp("".join(chars)))
            chars = insert_motifs(rng, chars, N_MOTIFS_PER_SEED)
            original = "".join(chars)
            f.write(original + "\n")
            written += 1
            for _ in range(N_VARS_PER_SEED - 1):
                v = make_variant(rng, original)
                f.write(v + "\n")
                written += 1
    print(f"Wrote {written} sequences ({N_SEEDS} seeds × {N_VARS_PER_SEED} variants)")

if __name__ == "__main__":
    main()
