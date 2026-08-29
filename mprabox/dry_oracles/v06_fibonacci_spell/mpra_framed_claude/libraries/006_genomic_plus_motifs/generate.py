"""
Experiment 006: chr22 random genomic + 2 embedded TF motifs per sequence.

Theory:
  Random genomic plateaus at ~0.134 (003). Plain motif insertion gave 0.124
  (002). What about combining them — natural context + explicit motif
  density? This should give the model BOTH realistic syntax AND clearer
  signal-per-sequence.

Design:
  - Random 200bp chr22 windows (as in 003).
  - For each window: embed 2 motifs from the 60-motif curated set at
    random non-overlapping positions, random orientation, OVERWRITING
    the underlying bases.
  - Seed=42.

Generalization rationale:
  Real genomic background carries the natural distribution the eval
  probably tests. Embedded motifs from a 60-TF set explicitly cover
  TFs from many cell-type families (hematopoietic, hepatic, neural,
  immune, developmental, ubiquitous), pushing the model to learn
  motif vocabulary broadly. The model is forced to attend to both
  natural cluster structure and explicit signal — a richer training
  distribution.
"""

import os
import random

N_SEQS = 50_000
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

def insert_motifs(rng, seq_chars, motifs, n):
    L = len(seq_chars)
    used = []
    for _ in range(n):
        m = rng.choice(motifs)
        if rng.random() < 0.5:
            m = revcomp(m)
        ml = len(m)
        for attempt in range(20):
            pos = rng.randrange(0, L - ml + 1)
            ok = True
            for s, e in used:
                if not (pos + ml <= s or pos >= e):
                    ok = False
                    break
            if ok:
                seq_chars[pos:pos + ml] = list(m)
                used.append((pos, pos + ml))
                break
    return seq_chars

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
    print(f"chr22 valid starts: {len(starts):,}")
    sampled = rng.sample(starts, N_SEQS)
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for s in sampled:
            w = chr22[s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            chars = list(w)
            chars = insert_motifs(rng, chars, MOTIFS, 2)
            f.write("".join(chars) + "\n")
    print(f"Wrote {N_SEQS} to {out}")

if __name__ == "__main__":
    main()
