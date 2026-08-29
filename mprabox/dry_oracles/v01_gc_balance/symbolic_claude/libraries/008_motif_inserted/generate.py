"""
Experiment 008: Motif-inserted random library.

50,000 unique sequences. Each = random background + 4 inserted motifs.
Motif pool covers several "biologically plausible" 6-mer patterns in our
alphabet:
  - Palindromic-like: '030303', '121212', '012012', '321321'
  - Asymmetric: '012321', '123210', '003300', '110022'
  - Mixed:      '012312', '321032', '230123', '102320'

The bet: motif insertions push sequences into the "high-information"
regime that the f, g predictors care about, raising correlation.
"""
import os, random

random.seed(8)

L = 200
N = 50000
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

motifs = [
    "030303", "121212", "012012", "321321",
    "012321", "123210", "003300", "110022",
    "012312", "321032", "230123", "102320",
]
M = len(motifs)
mlen = len(motifs[0])

lines = []
for _ in range(N):
    seq = list(random.choices(ALPHABET, k=L))
    # 4 motif insertions at random non-overlapping positions
    used = set()
    inserts = 0
    attempts = 0
    while inserts < 4 and attempts < 40:
        attempts += 1
        pos = random.randint(0, L - mlen)
        if any(p in used for p in range(pos, pos + mlen)):
            continue
        m = motifs[random.randint(0, M - 1)]
        for j, c in enumerate(m):
            seq[pos + j] = c
            used.add(pos + j)
        inserts += 1
    lines.append("".join(seq))

assert len(lines) == N

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} unique motif-inserted seqs")
