"""Experiment 028 — chr22 + chr19 + chr1 weighted mix (40/40/20).

Theory v9: scorer is correlation; library diversity helps. chr22+chr19
50/50 gave 0.3215 (new best). Try adding 20% chr1 (HepG2-best at
0.2020) for more diversity. chr1's lower GC may slightly drop SKNSH
but should add diversity & HepG2 reward.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(28)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
chrom_seq = {}
for name in ("chr22", "chr19", "chr1"):
    parts = []
    with (ROOT / "data" / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"): continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)

def sample(name, k):
    seq = chrom_seq[name]
    out = []
    while len(out) < k:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        out.append(s)
    return out

# 40% chr22, 40% chr19, 20% chr1
n22 = int(0.4 * N)
n19 = int(0.4 * N)
n1 = N - n22 - n19

all_seqs = sample("chr22", n22) + sample("chr19", n19) + sample("chr1", n1)
rng.shuffle(all_seqs)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for s in all_seqs:
        f.write(s); f.write("\n")
print(f"Wrote {len(all_seqs)} (chr22={n22}, chr19={n19}, chr1={n1})")
