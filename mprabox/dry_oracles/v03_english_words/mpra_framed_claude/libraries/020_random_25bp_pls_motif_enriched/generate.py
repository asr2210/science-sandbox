"""
020 — Random + 1x25bp PLS-only fragment SELECTED for canonical motif content.

Like 012 but candidate 25bp fragments are scored by canonical TF motif hits;
only fragments with >=1 motif are accepted. Same composition class as 012,
but denser motif content per fragment.

Motif panel (forward + revcomp):
- TATA box: TATAAA, TATAWA
- CCAAT box: CCAAT
- GC box / SP1: GGGCGG / CCGCCC
- Inr core: YYANWYY -> match CAGT/TCAGT
- E-box (NEUROD/MYC): CAGCTG, CACGTG
- REST core: TCAGCAC
- POU/Brn: ATGCAAAT
- NFkB: GGGRNTYYC -> match GGGACT
"""
import numpy as np
import re
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
FRAG_LEN = 25
SEED = 20

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

# Canonical motif consensuses; require at least one hit (forward or revcomp).
MOTIFS = [
    "TATAAA", "TATATA",
    "CCAAT", "ATTGG",          # CCAAT box + revcomp
    "GGGCGG", "CCGCCC",        # SP1 / GC-box
    "CAGCTG",                  # E-box (NEUROD/MYC) palindromic
    "CACGTG",                  # E-box (MYC) palindromic
    "TCAGCAC", "GTGCTGA",      # REST + revcomp
    "ATGCAAAT", "ATTTGCAT",    # POU + revcomp
    "GGGACTTTCC", "GGAAAGTCCC", # NFkB + revcomp
    "AGGTCA", "TGACCT",        # nuclear receptor + revcomp
    "GATAAG", "CTTATC",        # GATA + revcomp
]
motif_re = re.compile("|".join(MOTIFS))

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
seqs = [list(row) for row in bg]

pls = []
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK and etype == "PLS":
            pls.append((chrom, int(start), int(end)))

print(f"PLS pool size: {len(pls)}")

fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)

# Sample many candidate fragments, accept only motif-positive ones.
fragments = []
attempted = 0
chosen = rng.integers(0, len(pls), size=N * 8 + 5000)
for i in chosen:
    attempted += 1
    chrom, start, end = pls[i]
    mid = (start + end) // 2
    ws, we = mid - 100, mid + 100
    if ws < 0 or we > len(fa[chrom]):
        continue
    full = str(fa[chrom][ws:we]).upper()
    if len(full) != 200 or not set(full).issubset(ALPHA):
        continue
    f_start = int(rng.integers(0, 200 - FRAG_LEN + 1))
    frag = full[f_start:f_start + FRAG_LEN]
    if not set(frag).issubset(ALPHA):
        continue
    if motif_re.search(frag):
        fragments.append(frag)
    if len(fragments) >= N:
        break

print(f"PLS motif-enriched fragments collected: {len(fragments)} from {attempted} attempts")

positions = rng.integers(0, L - FRAG_LEN + 1, size=N)
for i in range(N):
    frag = fragments[i % len(fragments)]
    pos = int(positions[i])
    for j, ch in enumerate(frag):
        seqs[i][pos + j] = ch

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"wrote {N} x {L}bp random + 25bp PLS motif-enriched to {OUT}")
