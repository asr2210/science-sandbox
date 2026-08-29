"""Exp 017: Chimera with 10bp natural insert (vs Exp 015's 30bp).
Smallest dose, tests if even tiny natural inserts help SKNSH.
"""
import numpy as np, os

N = 50_000
L = 200
INSERT_LEN = 10
SEED = 17
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "data")
CHUNKS1 = os.path.join(BASE, "genome_chunks.txt")
CHUNKS2 = os.path.join(BASE, "genome_chunks_extra.tsv")

all_chunks = []
with open(CHUNKS1) as f:
    for line in f:
        s = line.strip()
        if s:
            all_chunks.append(s)
with open(CHUNKS2) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 4:
            all_chunks.append(parts[3])
cum = np.cumsum([len(c) for c in all_chunks])
total_bp = int(cum[-1])

inserts = []
attempts = 0
while len(inserts) < N and attempts < N * 10:
    attempts += 1
    pos = int(rng.integers(0, total_bp - INSERT_LEN))
    ci = int(np.searchsorted(cum, pos, side="right"))
    chunk_start = 0 if ci == 0 else int(cum[ci - 1])
    local = pos - chunk_start
    chunk = all_chunks[ci]
    if local + INSERT_LEN > len(chunk):
        continue
    sub = chunk[local:local + INSERT_LEN]
    if "N" in sub:
        continue
    inserts.append(sub)
assert len(inserts) == N

arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")
for i in range(N):
    pos = int(rng.integers(0, L - INSERT_LEN + 1))
    for k, ch in enumerate(inserts[i]):
        seqs[i, pos + k] = ch

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} chimera (10bp natural)")
