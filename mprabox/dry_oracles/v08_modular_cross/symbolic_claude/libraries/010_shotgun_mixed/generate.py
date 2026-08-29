"""Shotgun library: mix of 10 generation methods.

Aims to maximize within-library diversity along every axis I've considered:
composition, complexity, motif presence, periodicity, GC bias.

If diversity along multiple axes simultaneously is what the scorer wants, this should win.
"""
import numpy as np
import os

SEED = 71
N_PER = 5000
L = 200
ALPHA = "0123"
rng = np.random.default_rng(SEED)


def to_str(arr):
    return ["".join(ALPHA[c] for c in row) for row in arr]


def random_uniform(n):
    return rng.integers(0, 4, size=(n, L), dtype=np.uint8)


def dirichlet_alpha(n, alpha):
    probs = rng.dirichlet(np.full(4, alpha), size=n)
    out = np.empty((n, L), dtype=np.uint8)
    for i in range(n):
        out[i] = rng.choice(4, size=L, p=probs[i])
    return out


def markov_dna(n):
    T = np.array(
        [
            [0.30, 0.20, 0.29, 0.21],
            [0.32, 0.27, 0.04, 0.37],
            [0.30, 0.24, 0.27, 0.19],
            [0.18, 0.25, 0.30, 0.27],
        ]
    )
    stat = np.array([0.274, 0.239, 0.228, 0.259])
    out = np.empty((n, L), dtype=np.uint8)
    out[:, 0] = rng.choice(4, size=n, p=stat)
    for j in range(1, L):
        u = rng.random(size=n)
        cum = np.cumsum(T[out[:, j - 1]], axis=1)
        out[:, j] = (u[:, None] < cum).argmax(axis=1)
    return out


def kmer_repeats(n, k):
    def int_to_kmer(x, k):
        out = []
        for _ in range(k):
            out.append(x % 4)
            x //= 4
        return out[::-1]

    kmer_idx = rng.integers(0, 4**k, size=n)
    kmers = np.array([int_to_kmer(x, k) for x in kmer_idx], dtype=np.uint8)
    reps = L // k
    out = np.tile(kmers, (1, reps))
    extra = L - reps * k
    if extra > 0:
        out = np.concatenate([out, kmers[:, :extra]], axis=1)
    return out[:, :L]


def random_with_motif(n, motif_str):
    out = rng.integers(0, 4, size=(n, L), dtype=np.uint8)
    motif = np.array([int(c) for c in motif_str], dtype=np.uint8)
    pos = (L - len(motif)) // 2
    out[:, pos : pos + len(motif)] = motif
    return out


def biased_random(n, probs):
    return rng.choice(4, size=(n, L), p=probs).astype(np.uint8)


groups = [
    ("random_uniform", random_uniform(N_PER)),
    ("dirichlet_0p1", dirichlet_alpha(N_PER, 0.1)),
    ("dirichlet_1p0", dirichlet_alpha(N_PER, 1.0)),
    ("markov_dna", markov_dna(N_PER)),
    ("4mer_repeats", kmer_repeats(N_PER, 4)),
    ("8mer_repeats", kmer_repeats(N_PER, 8)),
    ("motif_01230123", random_with_motif(N_PER, "01230123")),
    ("motif_00033330", random_with_motif(N_PER, "00033330")),
    ("at_rich", biased_random(N_PER, [0.4, 0.1, 0.1, 0.4])),
    ("gc_rich", biased_random(N_PER, [0.1, 0.4, 0.4, 0.1])),
]

all_seqs = []
for name, arr in groups:
    all_seqs.extend(to_str(arr))
    print(f"{name}: {arr.shape[0]} seqs")

assert len(all_seqs) == 50000, len(all_seqs)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in all_seqs:
        f.write(s + "\n")

print(f"Wrote {len(all_seqs)} shotgun-mix sequences to {out_path}")
