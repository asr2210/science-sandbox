"""013_sat_mut.

50,000 = 2,500 cCREs × 20 sequences (1 WT + 19 mutants).
Each mutant has 5 random single-base substitutions (~2.5% per
sequence, scattered across the 200bp). This gives the model paired
WT/mutant training pairs from which it can learn per-position
contribution to activity.

Generalization rationale: per-position effect learning is the
fundamental atomic unit of regulatory grammar — universal across
cell types. A model that learns "this position carries motif info,
this one doesn't" learns rules that compose into cell-type-
agnostic prediction.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 2_500
SEQS_PER_REGION = 20  # 1 WT + 19 mutants
N_MUTS = 5  # substitutions per mutant
LEN = 200
HALF = LEN // 2
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

ALT = {
    "A": "CGT",
    "C": "AGT",
    "G": "ACT",
    "T": "ACG",
}

def mutate(seq, n_muts, rng):
    """Return a new sequence with n_muts random single-base
    substitutions at distinct random positions."""
    s = list(seq)
    positions = rng.choice(len(s), size=n_muts, replace=False)
    for p in positions:
        ref = s[p]
        if ref not in ALT:
            continue
        s[p] = ALT[ref][rng.integers(0, 3)]
    return "".join(s)


rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCRE midpoints on main chroms: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
region_order = rng.permutation(len(rows))

n_written = 0
n_regions_used = 0
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for idx in region_order:
        if n_regions_used >= N_REGIONS:
            break
        chrom, mid = rows[idx]
        s = mid - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            continue
        wt = fasta[chrom][s:e]
        if "N" in wt or len(wt) != LEN:
            continue
        # write WT
        f.write(wt)
        f.write("\n")
        n_written += 1
        # write 19 mutants
        for _ in range(SEQS_PER_REGION - 1):
            mutant = mutate(wt, N_MUTS, rng)
            f.write(mutant)
            f.write("\n")
            n_written += 1
        n_regions_used += 1

print(f"Wrote {n_written} from {n_regions_used} regions")
assert n_written == N_REGIONS * SEQS_PER_REGION == 50_000
