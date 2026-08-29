#!/usr/bin/env python3
"""Real human DNA from chr22, tiled as 200bp windows.

Skip N-rich regions. Sample 50K non-overlapping or randomly-positioned 200bp
windows from the non-N portion of chr22.
"""
import numpy as np
import os
from Bio import SeqIO

N = 50_000
L = 200
SEED = 42

REF = "data/chr22.fa"

rec = next(SeqIO.parse(REF, "fasta"))
s = str(rec.seq).upper()
print("chr22 len:", len(s))

# Find non-N regions
import re
non_n_spans = []
for m in re.finditer(r"[ACGT]{200,}", s):
    non_n_spans.append((m.start(), m.end()))
print(f"non-N spans (>=200bp): {len(non_n_spans)}, total bp: {sum(e-s for s,e in non_n_spans)}")

rng = np.random.default_rng(SEED)
seqs = []
# Sample positions uniformly across non-N coverage
total_eligible = sum(max(0, e - st - L + 1) for st, e in non_n_spans)
print("eligible start positions:", total_eligible)

# Build a flat list of eligible (span_start, max_offset)
cum = []
running = 0
for st, e in non_n_spans:
    elig = max(0, e - st - L + 1)
    if elig > 0:
        cum.append((st, elig, running))
        running += elig
total = running

# Sample uniformly without replacement (or with — 50K << total_eligible)
picks = rng.choice(total, size=N, replace=False)
picks.sort()

# Map back to actual positions
out_seqs = []
ci = 0
for p in picks:
    # advance ci
    while ci + 1 < len(cum) and cum[ci+1][2] <= p:
        ci += 1
    st, elig, base = cum[ci]
    offset = p - base
    seq = s[st + offset : st + offset + L]
    assert len(seq) == L and set(seq) <= set("ACGT"), seq
    out_seqs.append(seq)

# Shuffle so order is randomized
rng.shuffle(out_seqs)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_seqs) + "\n")
print(f"Wrote {len(out_seqs)} real-human-DNA sequences to {out}")
