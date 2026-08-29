"""Experiment 008: random 200bp windows from human chr21 (hg38).

If predictors were trained on real DNA, real genomic windows might engage
them more strongly than synthetic uniform random.

Filters: skip windows with any N's (centromeric/gap regions).
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FA  = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chr21.fa")
N, L = 50_000, 200

# Read chr21 (single record). Strip header + newlines.
with open(FA) as f:
    lines = f.readlines()
assert lines[0].startswith(">")
chr21 = "".join(line.strip() for line in lines[1:]).upper()
print(f"chr21 length: {len(chr21):,}")
gc = (chr21.count("C") + chr21.count("G")) / max(1, len(chr21) - chr21.count("N"))
print(f"chr21 GC content (excluding N): {gc:.3f}")
print(f"chr21 N count: {chr21.count('N'):,}")

rng = np.random.default_rng(8)
ok_chars = set("ACGT")
seqs = []
attempts = 0
while len(seqs) < N and attempts < N * 20:
    start = int(rng.integers(0, len(chr21) - L + 1))
    window = chr21[start:start + L]
    if set(window) <= ok_chars:
        seqs.append(window)
    attempts += 1

print(f"sampled {len(seqs)} windows in {attempts} attempts")
assert len(seqs) == N, f"only got {len(seqs)}"
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
# quick stats
gc_lib = sum((s.count("C") + s.count("G")) for s in seqs[:1000]) / (1000 * L)
print(f"library GC (first 1000): {gc_lib:.3f}")
print(f"first: {seqs[0][:80]}...")
