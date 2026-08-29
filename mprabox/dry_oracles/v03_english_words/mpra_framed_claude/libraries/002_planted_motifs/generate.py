"""
Random 200bp background with 3-5 canonical TF motifs planted per sequence.
Motif panel spans K562 (hematopoietic), HepG2 (hepatic), SK-N-SH (neural),
and broadly-active TFs.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 2
OUT = Path(__file__).parent / "sequences_0.txt"

# Canonical consensus motifs (no IUPAC ambiguity — pick a strong consensus).
# Curated from JASPAR/HOCOMOCO common TF cores; goal is broad coverage, not
# exact PWMs. Each entry is a (name, consensus) tuple.
MOTIFS = [
    # K562 / hematopoietic
    ("GATA1",   "AGATAAG"),
    ("GATA2",   "AGATAAG"),
    ("KLF1",    "CACCC"),
    ("MYB",     "AACTGTC"),
    ("RUNX1",   "TGTGGTT"),
    ("TAL1",    "CAGATG"),
    ("LMO2",    "CTGNAG".replace("N","A")),
    ("STAT5",   "TTCCAGGAA"),
    # HepG2 / hepatic
    ("HNF4A",   "AGGTCAAAGGTCA"),
    ("HNF1A",   "GTTAATCATTAAC"),
    ("HNF6",    "ATTGATTT"),
    ("CEBPA",   "ATTGCGCAAT"),
    ("FOXA1",   "TGTTTGT"),
    ("FOXA2",   "TGTTTAC"),
    ("ONECUT",  "ATCGAT"),
    ("PPARA",   "AGGTCAAAGGTCA"),
    # SK-N-SH / neural
    ("NEUROD1", "GCAGATGT"),
    ("ASCL1",   "CAGCTG"),
    ("REST",    "TTCAGCACCATGGACAG"),  # NRSE
    ("POU3F2",  "ATGCATAAT"),
    ("POU4F1",  "TAATGAATAATT"),
    ("PAX6",    "TTCACGCTT"),
    ("OLIG2",   "CAGCTG"),
    ("ATOH1",   "CAGCTG"),
    ("MEF2C",   "CTATAAATAG"),
    ("CRX",     "TAATCC"),
    ("ISL1",    "TAATCA"),
    ("DLX",     "TAATTA"),
    ("LHX2",    "TAATTA"),
    ("LMX1B",   "TAATTA"),
    ("NEUROG2", "CACATG"),
    ("TCF4",    "CACGTG"),
    # Broadly-active
    ("SP1",     "GGGGCGGGG"),
    ("NFY",     "CCAATCA"),
    ("ETS1",    "ACCGGAAGT"),
    ("ELK1",    "ACCGGAAGT"),
    ("AP1",     "TGACTCA"),
    ("CREB",    "TGACGTCA"),
    ("ATF",     "TGACGTCA"),
    ("YY1",     "CCATCTT"),
    ("NRF1",    "TGCGCATGCGCA"),
    ("USF",     "CACGTG"),
    ("E2F",     "TTTCCCGC"),
    ("TEAD",    "GGAATG"),
    ("MAX",     "CACGTG"),
    ("HSF",     "TTCTAGAA"),
    ("NFKB",    "GGGACTTTCC"),
    ("STAT1",   "TTCCCGGAA"),
    ("IRF",     "AAGTGAAA"),
    ("RUNX2",   "TGTGGTT"),
    ("MEIS1",   "TGACAG"),
    ("TBX",     "AGGTGTGA"),
    ("ZEB",     "CACCTG"),
    ("SNAI",    "CACCTG"),
    ("KLF4",    "GGGGCGGGG"),
    ("EGR1",    "GCGGGGGCG"),
    ("CTCF",    "CCGCGNGGNGGCAG".replace("N","A")),
    ("p53",     "GGACATGCCC"),
    ("SOX2",    "CATTGTT"),
    ("NANOG",   "ATTAACAAT"),
    ("OCT4",    "ATGCAAAT"),
]

MOTIF_SEQS = [m[1].upper() for m in MOTIFS]
assert all(set(s).issubset(set("ACGT")) for s in MOTIF_SEQS), "non-ACGT motif"

def revcomp(s):
    return s.translate(str.maketrans("ACGT","TGCA"))[::-1]

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

# Random backgrounds as a 2D byte array (write as char arrays then mutate).
bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
# Convert to list-of-lists once for in-place edits.
seqs = [list(row) for row in bg]

motif_count_per_seq = rng.integers(3, 6, size=N)  # 3-5 inclusive (high=6)
for i in range(N):
    k = int(motif_count_per_seq[i])
    chosen = rng.choice(len(MOTIF_SEQS), size=k, replace=True)
    # Place each motif at a non-overlapping random position when possible.
    used_intervals = []
    for mi in chosen:
        m = MOTIF_SEQS[mi]
        if rng.random() < 0.5:
            m = revcomp(m)
        mlen = len(m)
        if mlen > L:
            continue
        # Try a few positions to avoid heavy overlap.
        for _ in range(8):
            pos = int(rng.integers(0, L - mlen + 1))
            ok = all(not (pos < end and pos + mlen > start) for start, end in used_intervals)
            if ok:
                break
        used_intervals.append((pos, pos + mlen))
        for j, ch in enumerate(m):
            seqs[i][pos + j] = ch

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")

print(f"wrote {N} x {L}bp sequences with planted motifs to {OUT}")
print(f"motif panel size: {len(MOTIF_SEQS)} TFs")
