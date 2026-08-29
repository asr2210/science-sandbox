"""
Experiment 008: 50/50 mix of best two designs.
  - 25k chr22 random 200bp windows (003 style)
  - 25k chr22 random + 2 embedded TF motifs (006 style)

Theory:
  003 and 006 plateaued at ~0.134-0.135. A 50/50 mix tests whether
  combining two distributions (pure genomic + motif-augmented) helps
  beyond either alone. If yes → "distribution diversity" hypothesis is
  supported and bigger mixes (008+) should keep climbing. If no → 003
  is at the eval cap for unique-context random genomic.

Design:
  - 25,000 chr22 windows, random orientation, no motif insertion.
  - 25,000 chr22 windows, random orientation, +2 motifs from the
    60-motif set inserted at random non-overlapping positions.
  - 50,000 unique source windows (no overlap with each other).
  - Seed=42.

Generalization rationale:
  Mix exposes the model to two related distributions:
  (a) pure genomic — natural background frequency, realistic syntax.
  (b) genomic + extra motifs — same context, boosted signal.
  This combined training set should produce representations invariant
  to whether motifs are native or augmented — closer to learning the
  motif function abstractly. That function transfers across cell types.
"""

import os
import random

N_SEQS = 50_000
N_PURE = 25_000
N_AUGMENTED = 25_000
SEQ_LEN = 200
SEED = 42

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
            if all(pos + ml <= s or pos >= e for s, e in used):
                chars[pos:pos + ml] = list(m)
                used.append((pos, pos + ml))
                break
    return chars

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
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
    sampled = rng.sample(starts, N_SEQS)
    pure_starts = sampled[:N_PURE]
    aug_starts = sampled[N_PURE:]

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for s in pure_starts:
            w = chr22[s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
        for s in aug_starts:
            w = chr22[s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            chars = list(w)
            chars = insert_motifs(rng, chars, 2)
            f.write("".join(chars) + "\n")
    print(f"Wrote {N_PURE} pure + {N_AUGMENTED} augmented = {N_SEQS}")

if __name__ == "__main__":
    main()
