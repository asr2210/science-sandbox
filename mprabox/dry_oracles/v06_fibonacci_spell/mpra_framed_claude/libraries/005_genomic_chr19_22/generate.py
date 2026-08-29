"""
Experiment 005: random 200bp genomic windows from chr19 + chr22.

Theory:
  003 (chr22 random) = 0.134, 004 (chr19+22 cCRE) = 0.126. The cCRE
  enrichment surprised us by underperforming. This experiment isolates
  the chromosome question: does adding chr19 to chr22 help (more genomic
  diversity), or does chr19's GC bias / gene density hurt?

Design:
  Same as 003 but sample windows from chr19 AND chr22 combined.
  - Load both FASTAs, find non-N runs ≥200bp.
  - Sample 50,000 starts uniformly across all valid positions.
  - Random orientation. Seed=42.

Generalization rationale:
  Multi-chromosome genomic sampling provides broader sequence-distribution
  coverage than single-chromosome sampling, while preserving the natural
  active/inactive balance (no cCRE bias). Real human regulatory grammar
  isn't chromosome-specific; broader sampling captures more TFBS classes
  and contexts.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
FASTAS = ["data/chr19.fa", "data/chr22.fa"]

ALPHABET = set("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    chrom = None
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                chrom = line[1:].strip().split()[0]
            else:
                parts.append(line.strip().upper())
    return chrom, "".join(parts)

def main():
    rng = random.Random(SEED)
    # combined start list: (chrom_name, position)
    chrom_seqs = {}
    starts = []
    for fa in FASTAS:
        chrom, seq = load_fasta(fa)
        chrom_seqs[chrom] = seq
        L = len(seq)
        # find runs of valid bases
        i = 0
        while i < L:
            if seq[i] in ALPHABET:
                j = i
                while j < L and seq[j] in ALPHABET:
                    j += 1
                if j - i >= SEQ_LEN:
                    for s in range(i, j - SEQ_LEN + 1):
                        starts.append((chrom, s))
                i = j
            else:
                i += 1
        print(f"{chrom}: len={L:,}")
    print(f"Total valid 200bp starts: {len(starts):,}")
    sampled = rng.sample(starts, N_SEQS)
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for chrom, s in sampled:
            w = chrom_seqs[chrom][s:s + SEQ_LEN]
            if rng.random() < 0.5:
                w = revcomp(w)
            f.write(w + "\n")
    print(f"Wrote {N_SEQS} to {out}")

if __name__ == "__main__":
    main()
