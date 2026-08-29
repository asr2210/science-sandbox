"""
Experiment 002: 2-3 diverse TF motifs embedded in random 200bp backgrounds.

Theory:
  K562 was at ~0 mean_r on random sequences (Exp 001). Hypothesis: motif
  presence is the dominant signal a sequence-to-activity model needs. Embedding
  a diverse set of TF motifs across ~50 families should provide strong
  gradients across all three cell types while exposing the model to a motif
  vocabulary broader than any single cell type's TFs — supporting transfer to
  unmeasured cell types.

Design:
  - 50,000 sequences, 200bp each.
  - Each sequence: random ACGT background.
  - For each sequence, insert 2-3 motifs (uniformly sampled 2,3) at random
    non-overlapping positions.
  - For each motif insertion: pick a random TF from the 60-motif curated set,
    pick orientation (forward or reverse complement) uniformly at random.
  - Insertions overwrite background bases (do NOT shift).
  - Seed=42.

Generalization rationale:
  Motifs are conserved across cell types. A model that learns motif
  recognition learns a transferable function. The diverse 60-motif set spans
  TF families beyond K562/HepG2/SK-N-SH-specific TFs (includes neural,
  hematopoietic, hepatic, immune, developmental, ubiquitous), so the model is
  forced to learn a broad alphabet — not just the three cell types' favorites.
"""

import os
import random

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = "ACGT"
SEED = 42

# Curated TF motif consensus sequences. Diverse families:
# bHLH, bZIP, GATA, ETS, FOX, NF-kB, SP/KLF, MEF2, HNF, C/EBP, REST, HOX,
# POU, NFAT, STAT, IRF, p53, RUNX, SOX, TCF/LEF, MYB, NF-Y, CTCF, YY1, SRF,
# TBP, SMAD, TEAD, ZEB, nuclear receptors (ER/GR/AR/THR), HSF, E2F, NRF1,
# BACH, BCL6, PAX, NEUROD, ASCL, OCT, TBX, RUNX, EBF, PU.1, MEIS, GATA1,
# KLF4, IRF1, NRF2.
MOTIFS = [
    "CACGTG",         # E-box (MYC/USF/NEUROD1)
    "CAGCTG",         # E-box (ASCL1, neural)
    "CATCTG",         # E-box variant
    "TGACTCA",        # AP-1 (FOS/JUN)
    "TGAGTCA",        # AP-1 variant
    "TGACGTCA",       # CREB
    "AGATAA",         # GATA
    "TGATAA",         # GATA1
    "CCGGAAGT",       # ETS
    "ACCGGAAGT",      # ELK1
    "TGTTTAC",        # FOXO/FOXA
    "GTAAACA",        # FOX (reverse-related)
    "GGGAATTTCC",     # NF-kB (p65)
    "GGGGCGGGGC",     # SP1
    "CACCC",          # KLF
    "CTATAAATAG",     # MEF2
    "GTTAATCATTAAC",  # HNF1
    "AGGTCAAAGGTCA",  # HNF4 DR1
    "ATTGCGCAAT",     # C/EBP
    "TTCAGCACCATGGACAG",  # NRSF/REST
    "TAATCC",         # HOX (TAAT core)
    "ATGCAAAT",       # OCT/POU
    "GGAAA",          # NFAT
    "TTCCCGGAA",      # STAT
    "AAAGTGAAAGT",    # IRF
    "GGACATGTCC",     # p53 half-site
    "TGTGGT",         # RUNX core
    "AACAAAG",        # SOX (CATTGT reverse)
    "CTTTGTT",        # TCF/LEF
    "AACTGAC",        # MYB
    "CCAATCA",        # NF-Y CCAAT box
    "CCGCGNGGNGGCAG".replace("N",""),  # CTCF core (no N) -> CCGCGGGGGGCAG
    "CCATCTT",        # YY1
    "CCATATATGG",     # SRF CArG
    "TATAAAA",        # TATA box
    "AGTCTAGAC",      # SMAD palindrome
    "GGAATGTG",       # TEAD
    "CAGGTA",         # ZEB
    "AGGTCA",         # NR half-site (ER/GR/AR)
    "AGGTCATGACCT",   # THR DR0/IR
    "AGAACAGTGACCT",  # GR/AR-like
    "GAATTCTAGAA",    # HSF HSE
    "TTTCGCGC",       # E2F
    "GCGCATGCGC",     # NRF1
    "TGCTGAGTCAT",    # BACH/MAF AP-1-like
    "TTCCTAGAA",      # BCL6
    "GTCATGAT",       # PAX
    "AGCTGCT",        # NEUROD1/ASCL1
    "AGGTGT",         # TBX
    "ATCAATCA",       # PBX
    "CTAGTCCT",       # EBF
    "GGAAGTGA",       # PU.1
    "TGACAGGT",       # MEIS
    "AGGGTGTGGTCA",   # GATA1+E-box composite
    "CACCCT",         # KLF4
    "TTTCACTTTCC",    # IRF1
    "ATGACTCAGCA",    # NRF2/MAF ARE
    "CCCGCCCCC",      # GC-box SP-family extended
    "TGACCTTG",       # NR variant
    "GCTAATTGG",      # OCT4 variant
]

# Filter out anything not in {A,C,G,T}
MOTIFS = ["".join(c for c in m if c in ALPHABET) for m in MOTIFS]
MOTIFS = [m for m in MOTIFS if 4 <= len(m) <= 20]

COMPL = str.maketrans("ACGT", "TGCA")
def revcomp(s): return s.translate(COMPL)[::-1]

def random_seq(rng, n):
    return "".join(rng.choice(ALPHABET) for _ in range(n))

def insert_motifs(rng, seq_chars, motifs, n_insertions):
    """Pick n_insertions non-overlapping positions and overwrite with motifs."""
    L = len(seq_chars)
    used = []  # list of (start, end)
    for _ in range(n_insertions):
        motif = rng.choice(motifs)
        if rng.random() < 0.5:
            motif = revcomp(motif)
        ml = len(motif)
        # try a few random positions
        for attempt in range(20):
            pos = rng.randrange(0, L - ml + 1)
            ok = True
            for s, e in used:
                if not (pos + ml <= s or pos >= e):
                    ok = False
                    break
            if ok:
                seq_chars[pos:pos + ml] = list(motif)
                used.append((pos, pos + ml))
                break
    return seq_chars

def main():
    rng = random.Random(SEED)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for _ in range(N_SEQS):
            chars = list(random_seq(rng, SEQ_LEN))
            n_ins = rng.choice([2, 3])
            chars = insert_motifs(rng, chars, MOTIFS, n_ins)
            f.write("".join(chars) + "\n")
    print(f"Wrote {N_SEQS} sequences to {out_path}. {len(MOTIFS)} motifs.")

if __name__ == "__main__":
    main()
