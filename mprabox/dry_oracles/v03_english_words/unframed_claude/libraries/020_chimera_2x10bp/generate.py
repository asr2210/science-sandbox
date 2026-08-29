"""Exp 020: 2x 10bp natural inserts at random non-overlapping positions.
Tests if the 10bp insert benefit (Exp 017 = 0.4248) stacks additively.
"""
import numpy as np, os

N = 50_000
L = 200
INSERT_LEN = 10
NUM_INSERTS = 2
SEED = 20
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

def sample_insert():
    while True:
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
        return sub

inserts = [[sample_insert() for _ in range(NUM_INSERTS)] for _ in range(N)]

arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")
for i in range(N):
    # Sample 2 non-overlapping positions
    while True:
        p1 = int(rng.integers(0, L - INSERT_LEN + 1))
        p2 = int(rng.integers(0, L - INSERT_LEN + 1))
        if abs(p1 - p2) >= INSERT_LEN:
            break
    for p, ins in zip([p1, p2], inserts[i]):
        for k, ch in enumerate(ins):
            seqs[i, p + k] = ch

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} chimera (2x 10bp natural)")
