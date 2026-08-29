"""002_encode_ccre_uniform.

Sample 50,000 200bp windows centered on ENCODE V3 GRCh38 cCREs
(candidate cis-regulatory elements). Sampling is uniform across the
~1.06M cCREs of all classes (dELS, pELS, PLS, CTCF-only,
DNase-H3K4me3). cCREs were called from chromatin features across
hundreds of cell types — so the resulting library covers regulatory
grammar from many cellular contexts, not just K562/HepG2/SK-N-SH.

Rejects sequences containing N (assembly gap / unknown base).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_SEQS = 50_000
LEN = 200
HALF = LEN // 2
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"

# Load cCRE coordinates
print("Loading cCRE BED...")
rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        rows.append((chrom, int(start), int(end)))
print(f"Loaded {len(rows)} cCREs")

# Index FASTA
print("Indexing hg38...")
fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

# Keep only primary autosomes + X/Y/M (drop random/alt contigs for cleanliness)
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
rows = [r for r in rows if r[0] in KEEP_CHROMS]
print(f"After chrom filter: {len(rows)} cCREs")

rng = np.random.default_rng(SEED)
order = rng.permutation(len(rows))

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
n_skipped = 0
with open(out_path, "w") as f:
    for idx in order:
        if n_written >= N_SEQS:
            break
        chrom, start, end = rows[idx]
        center = (start + end) // 2
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            n_skipped += 1
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq:
            n_skipped += 1
            continue
        if len(seq) != LEN:
            n_skipped += 1
            continue
        f.write(seq)
        f.write("\n")
        n_written += 1

print(f"Wrote {n_written} sequences. Skipped {n_skipped}.")
assert n_written == N_SEQS, f"Got {n_written}, expected {N_SEQS}"
