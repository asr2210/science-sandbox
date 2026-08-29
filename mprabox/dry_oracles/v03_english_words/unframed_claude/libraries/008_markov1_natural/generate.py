"""Exp 008: 1st-order Markov from human dinucleotide frequencies.
Compute di-frequencies from data/genome_chunks.txt, then sample 50k
200bp sequences using a 1st-order Markov chain.
Preserves natural composition (mono + di) but destroys higher-order motifs.
"""
import numpy as np, os

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data",
                    "genome_chunks.txt")
N = 50_000
L = 200
SEED = 8
rng = np.random.default_rng(SEED)
bases = list("ACGT")
b2i = {b: i for i, b in enumerate(bases)}

# Count mono and di
mono = np.zeros(4)
di = np.zeros((4, 4))
with open(DATA) as f:
    for line in f:
        line = line.strip().upper()
        for i, c in enumerate(line):
            if c not in b2i:
                continue
            mono[b2i[c]] += 1
            if i + 1 < len(line) and line[i + 1] in b2i:
                di[b2i[c], b2i[line[i + 1]]] += 1

mono /= mono.sum()
trans = di / di.sum(axis=1, keepdims=True)
print("Mono freqs (A,C,G,T):", np.round(mono, 4))
print("Transition matrix (rows=from):")
print(np.round(trans, 4))
print("GC of stationary distribution:", mono[1] + mono[2])

# Sample sequences
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        seq = [0] * L
        seq[0] = rng.choice(4, p=mono)
        for j in range(1, L):
            seq[j] = rng.choice(4, p=trans[seq[j - 1]])
        f.write("".join(bases[i] for i in seq) + "\n")
print(f"Wrote {N} Markov-1 natural sequences")
