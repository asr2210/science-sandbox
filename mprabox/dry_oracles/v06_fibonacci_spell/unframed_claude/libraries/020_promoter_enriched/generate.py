"""Experiment 020: Promoter-enriched library from ENCODE cCREs.

Use only PLS (promoter-like signature) and DNase-H3K4me3 cCREs
(TSS-proximal regulatory elements). Distinct from exp 005, which used
ALL cCREs (dominated by 510k dELS distal enhancers).

Hypothesis: pure cCRE failed (0.1285) because it's mostly distal
enhancers. Promoter-only enrichment may match scorer's test distribution
better. With ~67k PLS+H3K4me3 we have enough to sample 50k.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 20

ROOT = Path(__file__).parents[2]
DATA = ROOT / "data"

# Parse cCREs, keep promoter-like only
promoter_keep = {"PLS", "PLS,CTCF-bound", "DNase-H3K4me3", "DNase-H3K4me3,CTCF-bound"}
entries = []
with open(DATA / "cCREs.bed") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[5] in promoter_keep:
            entries.append((parts[0], int(parts[1]), int(parts[2])))
print(f"Loaded {len(entries)} promoter-like cCREs")

with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

rng = np.random.default_rng(SEED)
valid = set("ACGT")
# Shuffle for sampling order
idx = np.arange(len(entries))
rng.shuffle(idx)

out = []
i = 0
attempts = 0
while len(out) < N and attempts < len(entries) * 3:
    attempts += 1
    if i >= len(idx):
        # Re-shuffle for second pass (samples with different offset)
        rng.shuffle(idx)
        i = 0
    c, s, e = entries[idx[i]]
    i += 1
    if c not in chroms:
        continue
    center = (s + e) // 2
    pos = center - L // 2
    if pos < 0 or pos + L > len(chroms[c]):
        continue
    # Small jitter so re-visits give different windows
    jit = int(rng.integers(-30, 31))
    p = max(0, min(len(chroms[c]) - L, pos + jit))
    w = chroms[c][p:p + L]
    if set(w) <= valid:
        out.append(w)

assert len(out) == N, f"got {len(out)} after {attempts} attempts"

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} promoter-enriched windows")
