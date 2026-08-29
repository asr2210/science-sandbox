"""Same sequences as exp 001 (random uniform seed=42) but sorted by GC content.
Tests whether the order of sequences within the library affects scoring."""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"
seqs = []
for _ in range(N):
    s = "".join(random.choice(ALPHA) for _ in range(L))
    seqs.append(s)
# Sort by GC content (chars 1 and 2)
seqs.sort(key=lambda s: s.count("1") + s.count("2"))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} sequences sorted by GC")
