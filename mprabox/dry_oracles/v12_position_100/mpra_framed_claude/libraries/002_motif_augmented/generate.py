"""Experiment 002: Motif-augmented random background.

Each 200bp sequence has a random uniform background, with 1-5 known TF
consensus motifs embedded at random positions and orientations.

Hypothesis: real TF binding sites in flanking random context give the
model the universal regulatory grammar (TFs bind by sequence, not by
cell type), so a sequence-to-activity model trained on this should
beat random uniform across all eval sets — including held-out cell
types we never measure.

Generalization rationale: the model learns "this motif drives activity"
from motif presence/absence variation in training. TF binding is a
universal property, so this learned association transfers to any cell
type whose activity is driven by these same TF families.
"""
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 2

# Curated list of ~60 well-known human TF binding motifs as consensus
# (IUPAC codes) — major TF families, varied lengths 5-15bp, representing
# the dominant regulatory grammar in human cells.
IUPAC_MOTIFS = [
    # AP-1 family (FOS/JUN heterodimers)
    "TGASTCA", "TGACTCA", "TGAGTCA",
    # CREB/ATF
    "TGACGTCA", "ATGACGTCAT",
    # bHLH / E-box (MYC, MAX, USF, NEUROD)
    "CACGTG", "CAGCTG", "CATGTG", "CANNTG",
    # ETS family (PU.1, GABPA, ELK, ETS1)
    "ACCGGAAGT", "CCGGAAGT", "GGAA", "AGGAAG",
    # SP1 / KLF (GC-box)
    "GGGGCGGGG", "CCCCGCCCC", "GGGGGCGGGG",
    # NF-kB / Rel
    "GGGRNYYYCC", "GGGACTTTCC", "GGGGATTCCC",
    # GATA factors
    "AGATAA", "WGATAR", "GATAA",
    # HNF / liver factors
    "CAAAGTCCA", "TGAACTTTG", "RGTTTGYTTY",
    # C/EBP
    "TTGCGCAAT", "ATTGCGCAAT", "TTGCGYAAT",
    # TEAD (Hippo pathway)
    "GGAATG", "CATTCC", "ACATTCC",
    # p53
    "RRRCWWGYYY", "GGACATGCCC",
    # NRF / antioxidant
    "TGCTGAGTCAT", "ATGACTCAGCA",
    # FOX family
    "TGTTTGT", "TGTTTAC", "GTAAACA",
    # TCF/LEF (Wnt)
    "CTTTGTT", "CTTTGAA", "AGATCAAAG",
    # STAT family
    "TTCYNRGAA", "TTCCCGGAA",
    # NFY (CCAAT box)
    "RRCCAATSR", "CCAATCAGA",
    # SRF (CArG box)
    "CCATATATGG", "CCWWWWWWGG",
    # MEF2
    "YTAWAAATAR", "CTATTTATAG",
    # IRF (interferon)
    "AANNGAAA", "AAANNGAAA",
    # HOX/HD
    "TAATTA", "TAATTG", "ATTA",
    # CTCF
    "CCGCGNGGNGGCAG", "CCCTC",
    # YY1
    "CGCCATNTT", "CCATCTT",
    # MYB
    "YAACKG", "CAGTTG",
    # ZNF / KLF
    "AGGGTGGGGC",
    # RUNX
    "TGTGGT", "ACCACA",
    # RFX (X-box)
    "GTTGCC", "GGCAAC",
    # NR (HNF4-like)
    "AGGTCANAGGTCA",
]

IUPAC = {
    "A": "A", "C": "C", "G": "G", "T": "T",
    "R": "AG", "Y": "CT", "S": "GC", "W": "AT",
    "K": "GT", "M": "AC", "B": "CGT", "D": "AGT",
    "H": "ACT", "V": "ACG", "N": "ACGT",
}
RC = str.maketrans("ACGT", "TGCA")


def realize(motif: str, rng: np.random.Generator) -> str:
    """Realize an IUPAC consensus into a concrete ACGT sequence."""
    out = []
    for ch in motif:
        choices = IUPAC[ch]
        out.append(choices[rng.integers(0, len(choices))])
    return "".join(out)


def make_sequence(rng: np.random.Generator, motif_pool: list) -> str:
    bases = np.array(list("ACGT"))
    seq = list(bases[rng.integers(0, 4, size=L)])
    n_motifs = rng.integers(1, 6)  # 1..5 motifs per sequence
    # Pick motifs (with replacement) and place them at non-overlapping positions
    placed_spans = []
    for _ in range(n_motifs):
        motif_template = motif_pool[rng.integers(0, len(motif_pool))]
        realized = realize(motif_template, rng)
        # 50% chance reverse complement
        if rng.integers(0, 2) == 1:
            realized = realized.translate(RC)[::-1]
        mlen = len(realized)
        if mlen >= L:
            continue
        # Try up to 10 placements, pick the first non-overlapping
        for _try in range(10):
            pos = int(rng.integers(0, L - mlen + 1))
            span = (pos, pos + mlen)
            if not any(s < span[1] and span[0] < e for s, e in placed_spans):
                for i, b in enumerate(realized):
                    seq[pos + i] = b
                placed_spans.append(span)
                break
    return "".join(seq)


def main():
    rng = np.random.default_rng(SEED)
    with open(OUT, "w") as f:
        for _ in range(N):
            f.write(make_sequence(rng, IUPAC_MOTIFS))
            f.write("\n")
    print(f"wrote {N} sequences of length {L} to {OUT}")


if __name__ == "__main__":
    main()
