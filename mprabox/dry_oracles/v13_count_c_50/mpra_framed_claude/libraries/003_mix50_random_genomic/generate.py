"""Experiment 003: 50/50 mixture of uniform random + random genomic.

Tests theory v2: heterogeneous libraries can span both the compositional and
grammatical axes simultaneously. Predict: eval_01 stays high (grammar
retained) AND eval_08 recovers (composition retained).

25,000 uniform-random 200bp sequences + 25,000 random hg38 chr19 windows.
Order shuffled so the model sees them interleaved during training.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
N_HALF = N // 2
FASTA = Path(__file__).resolve().parents[2] / "data" / "hg38.chr19.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)

bases = np.array(list("ACGT"))
rand_idx = rng.integers(0, 4, size=(N_HALF, L), dtype=np.uint8)
rand_seqs = ["".join(row.tolist()) for row in bases[rand_idx]]

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
chrom = "chr19"
seq_len = len(fa[chrom])
valid = set("ACGT")
gen_seqs = []
while len(gen_seqs) < N_HALF:
    batch = rng.integers(0, seq_len - L, size=4 * (N_HALF - len(gen_seqs)))
    for start in batch:
        if len(gen_seqs) >= N_HALF:
            break
        s = fa[chrom][int(start):int(start) + L]
        if len(s) == L and set(s).issubset(valid):
            gen_seqs.append(s)

all_seqs = rand_seqs + gen_seqs
rng.shuffle(all_seqs)
assert len(all_seqs) == N

with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences: 25k random + 25k chr19 genomic (shuffled).")
