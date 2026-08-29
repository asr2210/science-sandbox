"""Experiment 006: synthetic motif injection on random background.

50,000 sequences. Each = uniform random 200bp ACGT, then 2-5 well-known
TF binding sites are injected at random non-overlapping positions.
Random strand orientation for each motif.

Motif set: ~25 broadly-conserved mammalian TFBSs (TATA, CAAT, Sp1,
CREB, AP-1, NF-κB, E-box, GATA, HNF4, p53, FOX, POU, ETS, RUNX,
CTCF, NR half-sites, etc.). These TFs are expressed in essentially
all human cell types (with differential abundance) so motif knowledge
generalizes to any cell type.

Compares to:
- 001 (random uniform):    0.343 — no motifs at all
- 002 (genomic random):    0.497 — natural motifs + composition
- 003 (dinuc-shuffled):    0.436 — natural composition, no motifs
- 004 (cCREs):             0.386 — motif-enriched, composition-shifted

If 006 > 002: explicit motif density beats natural sequences
If 006 ≈ 002: motifs can substitute for natural genomic statistics
If 006 < 002: natural sequence statistics carry more than motifs
"""
import os
import random
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42

HERE = Path(__file__).parent

# Well-known mammalian TFBSs (consensus / core). All forward-strand;
# the generator picks random strand per insertion.
MOTIFS = [
    "TATAAA",          # TATA box
    "CCAATCT",         # CAAT box (extended)
    "GGGCGGGG",        # Sp1/GC box
    "TGACGTCA",        # CREB
    "TGACTCA",         # AP-1 (TGASTCA)
    "GGGACTTTCC",      # NF-kB consensus
    "CACGTG",          # E-box (Myc/USF/Max)
    "ATTGCGCAAT",      # C/EBP
    "AGATAAG",         # GATA
    "GGGCATGCCC",      # p53 half-decamer
    "GTTAATGATTAAC",   # HNF1 (palindrome)
    "AGGTCAAAGGTCA",   # HNF4 direct repeat (DR1-like)
    "AACAATGG",        # SOX (HMG)
    "TTCCCAGAA",       # STAT (GAS)
    "AGGTGTGA",        # TBX/T-box
    "TGTTTAC",         # FOXA / Forkhead core
    "ATGCAAAT",        # POU / OCT
    "TAATTA",          # HOX core
    "ACCGGAAGT",       # ETS (extended)
    "TGTGGTC",         # RUNX
    "CCCTCTAGTGGCC",   # CTCF core (zinc finger)
    "TTCAGCACCATGG",   # NRSF/REST RE1
    "AGGTCA",          # NR half-site
    "GAGGAA",          # ETS short
    "TTGTTT",          # NF-Y partial
    "GCCNNNGGC",       # GC tract / Sp1-related — N's replaced randomly per use
    "CACCTG",          # E-box variant (TCF/LEF)
    "GGAAGTG",         # IRF
    "TGASTCA",         # AP-1 variant (S = C/G)
    "WGATAR",          # GATA degenerate (W=A/T, R=A/G)
]

# Map IUPAC ambiguity to random expansion at injection time
IUPAC = {
    "A": "A", "C": "C", "G": "G", "T": "T",
    "W": "AT", "S": "CG", "R": "AG", "Y": "CT",
    "K": "GT", "M": "AC", "B": "CGT", "D": "AGT",
    "H": "ACT", "V": "ACG", "N": "ACGT",
}

def realize(motif, rng):
    out = []
    for c in motif:
        opts = IUPAC[c]
        out.append(rng.choice(opts))
    return "".join(out)

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def main():
    rng = random.Random(SEED)
    alphabet = "ACGT"

    seqs = []
    motif_count_histogram = {}
    for i in range(N_SEQ):
        backbone = [rng.choice(alphabet) for _ in range(LEN)]
        n_motifs = rng.randint(2, 5)
        # Try to place each motif at a random non-overlapping position
        occupied = []
        placed = 0
        for _ in range(n_motifs * 3):  # up to 3x tries
            if placed >= n_motifs:
                break
            mtemplate = rng.choice(MOTIFS)
            m = realize(mtemplate, rng)
            if rng.random() < 0.5:
                m = revcomp(m)
            mlen = len(m)
            if mlen > LEN:
                continue
            start = rng.randrange(0, LEN - mlen + 1)
            end = start + mlen
            # Check overlap with previous placements (simple linear scan)
            overlap = False
            for (a, b) in occupied:
                if not (end <= a or start >= b):
                    overlap = True
                    break
            if overlap:
                continue
            occupied.append((start, end))
            for j, ch in enumerate(m):
                backbone[start + j] = ch
            placed += 1
        motif_count_histogram[placed] = motif_count_histogram.get(placed, 0) + 1
        seqs.append("".join(backbone))

    print("Motifs placed histogram:", sorted(motif_count_histogram.items()))

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote {len(seqs)} sequences to {out_path}")

if __name__ == "__main__":
    main()
