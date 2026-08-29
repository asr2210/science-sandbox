"""
014 — Random + 1x25bp PLS fragment CENTERED on the cCRE midpoint.

Same as 012 but instead of a random 25bp offset within the 200bp window,
we take the 25bp centered exactly on the PLS midpoint (positions 88-112
of the 200bp window). PLS coords mark the regulatory core, so a centered
slice should consistently capture core promoter motifs (Inr, TATA, etc.).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
FRAG_LEN = 25
SEED = 14

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

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

# Sample PLS regions and extract the 25bp centered on each midpoint.
fragments = []
chosen = rng.integers(0, len(pls), size=N + 5000)
half = FRAG_LEN // 2  # 12
for i in chosen:
    chrom, start, end = pls[i]
    mid = (start + end) // 2
    fs, fe = mid - half, mid - half + FRAG_LEN  # 25bp centered
    if fs < 0 or fe > len(fa[chrom]):
        continue
    frag = str(fa[chrom][fs:fe]).upper()
    if len(frag) != FRAG_LEN or not set(frag).issubset(ALPHA):
        continue
    fragments.append(frag)
    if len(fragments) >= N:
        break

print(f"PLS centered fragments collected: {len(fragments)}")

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
print(f"wrote {N} x {L}bp random + 25bp PLS-centered fragments to {OUT}")
