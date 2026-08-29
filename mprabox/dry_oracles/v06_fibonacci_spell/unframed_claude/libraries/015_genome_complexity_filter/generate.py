"""Experiment 015: Full-genome random, with low-complexity filter.

Reject windows with low Shannon entropy or repetitive 8-mers (DUST-like).
Goal: remove uninformative simple-repeat/low-complexity sequences and
increase per-sequence k-mer information content.
"""
import pickle
import numpy as np
from pathlib import Path
from collections import Counter

N = 50_000
L = 200
SEED = 15
K = 6  # k-mer size for complexity scoring

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")

# Pre-pass: estimate threshold from 10k random windows
def kmer_entropy(s, k=K):
    c = Counter(s[i:i + k] for i in range(len(s) - k + 1))
    total = sum(c.values())
    probs = np.array([v / total for v in c.values()])
    return float(-np.sum(probs * np.log2(probs)))

probe = []
while len(probe) < 10_000:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    if set(w) <= valid:
        probe.append(kmer_entropy(w))
probe = np.array(probe)
print(f"random 6-mer entropy: mean={probe.mean():.3f}, std={probe.std():.3f}, "
      f"p10={np.percentile(probe, 10):.3f}, p50={np.percentile(probe, 50):.3f}")

# Take top-quartile entropy = drop the lowest-complexity 25%
threshold = float(np.percentile(probe, 25))
print(f"using entropy threshold > {threshold:.3f}")

# Main sampling
out = []
attempts = 0
while len(out) < N:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    attempts += 1
    if not (set(w) <= valid):
        continue
    if kmer_entropy(w) < threshold:
        continue
    out.append(w)

print(f"Took {attempts} attempts for {N} high-complexity windows")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {N} sequences (entropy-filtered)")
