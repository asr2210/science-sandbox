"""008_ccre_plus_random.

50,000 = 25,000 cCRE 200bp windows + 25,000 uniform random 200bp.
Tests whether composition spread (random) and regulatory grammar
(cCRE) are additive. Random sequences add max-entropy compositional
diversity that cCREs lack.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_HALF = 25_000
LEN = 200
HALF = LEN // 2
SEED = 0

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA / "GRCh38-cCREs.bed"
GENOME = DATA / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

# 1) Random half
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
rand_idx = rng.integers(0, 4, size=(N_HALF, LEN))
random_seqs = ["".join(row.tolist()) for row in bases[rand_idx]]

# 2) cCRE half
rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCREs available: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

order = rng.permutation(len(rows))
ccre_seqs = []
for idx in order:
    if len(ccre_seqs) >= N_HALF:
        break
    chrom, mid = rows[idx]
    s = mid - HALF
    e = s + LEN
    if s < 0 or e > chrom_lens[chrom]:
        continue
    seq = fasta[chrom][s:e]
    if "N" in seq or len(seq) != LEN:
        continue
    ccre_seqs.append(seq)
print(f"Got {len(ccre_seqs)} cCREs")

# Combine and shuffle order so they're interleaved
all_seqs = random_seqs + ccre_seqs
order2 = rng.permutation(len(all_seqs))
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for idx in order2:
        f.write(all_seqs[idx])
        f.write("\n")
print(f"Wrote {len(all_seqs)} sequences")
