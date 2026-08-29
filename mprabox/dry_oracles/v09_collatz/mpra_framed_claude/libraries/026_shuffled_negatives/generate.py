"""026_shuffled_negatives.

5K cCREs x 5 narrow tiles (positives, +/-100bp)
+ 5K cCRE tiles dinucleotide-shuffled (negatives, matched
  dinucleotide composition, no motif structure)
= 50K.

Direct comparison with 024 (real non-cCRE genomic negatives).
Tests whether the K562 bump in 024 comes from:
  (A) real intergenic genomic context (negatives carry useful
      non-regulatory genomic information)
  (B) non-functional sequence in general (matched composition
      with no motifs is enough)

Dinucleotide shuffling preserves CpG, dinucleotide frequencies
(critical for regulatory DNA which has distinct dinucleotide
patterns) but destroys motifs and longer-range structure.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_POS = 5_000
TILES_PER = 5
LEN = 200
HALF = LEN // 2
OFFSET = 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def dinuc_shuffle(seq, rng):
    """Altschul-Erikson dinucleotide shuffle (Eulerian path on
    dinuc graph). Preserves single AND dinucleotide composition.
    Simple implementation: random Eulerian walk through dinuc graph.
    """
    n = len(seq)
    if n < 4:
        return seq
    # build dinuc adjacency list
    adj = {}
    for i in range(n - 1):
        a = seq[i]
        b = seq[i + 1]
        adj.setdefault(a, []).append(b)
    # repeatedly try to construct walk; restart if stuck
    for _ in range(50):
        result = [seq[0]]
        local_adj = {k: list(v) for k, v in adj.items()}
        for k in local_adj:
            rng.shuffle(local_adj[k])
        ok = True
        for _ in range(n - 1):
            curr = result[-1]
            if curr not in local_adj or len(local_adj[curr]) == 0:
                ok = False
                break
            nxt = local_adj[curr].pop()
            result.append(nxt)
        if ok:
            return "".join(result)
    return seq  # fallback if no walk found


rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

import random
py_rng = random.Random(SEED)
rng = np.random.default_rng(SEED)
region_order = rng.permutation(len(rows))

positives = []
negatives = []
n_used = 0
for idx in region_order:
    if n_used >= N_POS:
        break
    chrom, mid = rows[idx]
    offsets = rng.integers(-OFFSET, OFFSET + 1, size=TILES_PER)
    tile_seqs = []
    for off in offsets:
        center = mid + int(off)
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            continue
        tile_seqs.append(seq)
    if len(tile_seqs) < TILES_PER:
        continue
    positives.extend(tile_seqs)
    # one shuffle per positive tile
    for s in tile_seqs:
        negatives.append(dinuc_shuffle(s, py_rng))
    n_used += 1

print(f"Positives: {len(positives)} from {n_used} cCREs")
print(f"Negatives (dinuc-shuffled): {len(negatives)}")

combined = positives + negatives
rng.shuffle(combined)
assert len(combined) == 50_000, f"got {len(combined)}"

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)} to {out_path.name}")
