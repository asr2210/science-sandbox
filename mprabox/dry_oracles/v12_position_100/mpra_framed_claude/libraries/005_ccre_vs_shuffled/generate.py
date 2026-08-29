"""Experiment 005: Real cCREs + dinucleotide-matched Markov controls.

50,000 sequences:
- 25,000 real cCREs (balanced across PLS/pELS/dELS/CA_TF/CA-CTCF)
- 25,000 Markov-generated sequences matching the dinucleotide
  composition of the cCRE pool (so same GC content and same
  dinucleotide frequencies, but motifs are scrambled)

Direct hypothesis test: if the cCRE advantage over random uniform comes
from MOTIFS / cis-regulatory grammar, the Markov half will be useless
training data and the library will underperform pure cCREs. If the
advantage comes from base composition (GC, CpG depletion, etc.), the
Markov half will be informative training data and performance should
match or exceed pure cCREs.

Generalization argument: this is a diagnostic experiment, not an
optimization. The point is to learn what makes cCREs valuable so
future libraries can amplify that property.
"""
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
BED = ROOT / "data" / "cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 5

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

# 25K real cCREs across classes
REAL_TARGETS = {
    "dELS":    8_000,
    "pELS":    6_000,
    "PLS":     4_000,
    "CA_TF":   4_000,
    "CA-CTCF": 3_000,
}
N_MARKOV = 25_000


def window_around(start, end, contig_len):
    mid = (start + end) // 2
    s = mid - L // 2
    e = s + L
    if s < 0:
        s, e = 0, L
    if e > contig_len:
        e, s = contig_len, contig_len - L
    return s, e


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_bed(path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def build_dinuc_transition(seqs):
    """Markov order-1 transition matrix from a list of sequences."""
    bases = "ACGT"
    b2i = {b: i for i, b in enumerate(bases)}
    counts = np.ones((4, 4), dtype=np.float64)  # +1 smoothing
    init_counts = np.ones(4, dtype=np.float64)
    for s in seqs:
        init_counts[b2i[s[0]]] += 1
        for i in range(len(s) - 1):
            counts[b2i[s[i]], b2i[s[i + 1]]] += 1
    trans = counts / counts.sum(axis=1, keepdims=True)
    init = init_counts / init_counts.sum()
    return init, trans


def markov_generate(init, trans, n, length, rng):
    bases = np.array(list("ACGT"))
    # Vectorized chain generation
    out = np.empty((n, length), dtype=np.uint8)
    out[:, 0] = rng.choice(4, size=n, p=init)
    for pos in range(1, length):
        prev = out[:, pos - 1]
        # For each row, sample next state from trans[prev[i]]
        # Vectorize: use cumulative distribution per prev
        u = rng.random(n)
        cdf = np.cumsum(trans, axis=1)  # shape (4,4)
        # next = first index where cdf[prev] > u
        thresh = cdf[prev]
        out[:, pos] = (u[:, None] < thresh).argmax(axis=1)
    seqs = ["".join(bases[row].tolist()) for row in out]
    return seqs


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class = {k: [] for k in REAL_TARGETS}
    for chrom, s, e, t in parse_bed(BED):
        if t == "PLS": grp = "PLS"
        elif t == "pELS": grp = "pELS"
        elif t == "dELS": grp = "dELS"
        elif t == "CA-CTCF": grp = "CA-CTCF"
        else: grp = "CA_TF"
        by_class[grp].append((chrom, s, e))
    for k, v in by_class.items():
        print(f"  {k}: {len(v):,} elements")

    real_seqs = []
    for grp, target in REAL_TARGETS.items():
        pool = by_class[grp]
        rng.shuffle(pool)
        added = 0
        seen = set()
        for chrom, s, e in pool:
            if added >= target:
                break
            ws, we = window_around(s, e, contig_lens[chrom])
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            real_seqs.append(seq)
            added += 1
        print(f"  {grp}: real added {added}/{target}")

    print("building dinucleotide transition from real cCREs...")
    init, trans = build_dinuc_transition(real_seqs)
    print(f"  init dist: {init}")
    print(f"  P(A|A)={trans[0,0]:.3f}  P(C|A)={trans[0,1]:.3f}  "
          f"P(G|C)={trans[1,2]:.3f}  P(T|T)={trans[3,3]:.3f}")

    print(f"generating {N_MARKOV} Markov controls...")
    markov_seqs = markov_generate(init, trans, N_MARKOV, L, nprng)

    all_seqs = real_seqs + markov_seqs
    if len(all_seqs) != N:
        raise RuntimeError(f"got {len(all_seqs)} != {N}")

    rng.shuffle(all_seqs)
    with open(OUT, "w") as f:
        for s in all_seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
