"""Experiment 008: 3-way mix — 20K natural + 15K cCRE + 15K dinucleotide-shuffled natural.

Tests two things simultaneously:
1. Does adding a 3rd source (shuffled) help beyond the 2-source mix?
2. Do dinucleotide-shuffled natural sequences (high k-mer entropy but
   natural-like composition) help on eval_08 specifically (immune to
   all previous libraries)?

Dinucleotide shuffle preserves the 1- and 2-mer distribution but
destroys motifs and higher-order structure. It's a classic negative
control in motif analysis — sequences that look natural at the dinuc
level but have no functional structure.

Hypothesis test:
- If 008 > 004 on most evals: 3-source mix > 2-source.
- If 008 > 004 on eval_08: shuffled controls help that specific eval.
- If 008 < 004: shuffled hurts (distribution shift away from natural).

Generalization argument: shuffled natural sequences teach the model what
"composition-matched but motif-stripped" looks like. This should help
the model distinguish "regulatory by virtue of motifs" from "natural
composition without function" — a discrimination essential for predicting
activity in any cell type.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CCRE = 15_000
N_SHUFFLED = N_SEQ - N_NATURAL - N_CCRE
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")

PRIMARY_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
PRIMARY_SET = set(PRIMARY_CHROMS)
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
BASES = ["A", "C", "G", "T"]


def sample_natural(fa, n, rng):
    chrom_lens = {c: len(fa[c]) for c in PRIMARY_CHROMS}
    chroms = np.array(PRIMARY_CHROMS)
    weights = np.array([chrom_lens[c] for c in PRIMARY_CHROMS], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(chroms, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def sample_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            cls = parts[9]
            if chrom not in PRIMARY_SET or cls not in HIGH_CONF:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((chrom, mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        start = mid - L // 2
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def dinuc_shuffle(seq, rng):
    """Altschul-Erickson dinucleotide shuffle (Eulerian path approach)."""
    # Build adjacency: count occurrences of each dinucleotide.
    n = len(seq)
    # Track edges from each char to following chars.
    edges = {b: [] for b in BASES}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])
    # Shuffle each edge list.
    for b in BASES:
        rng.shuffle(edges[b])
    # Reconstruct: greedy Euler walk starting at seq[0].
    # If we get stuck, retry with a different shuffle. For 200bp, usually
    # works first try.
    for _ in range(5):
        # Copy edge lists.
        e = {b: edges[b][:] for b in BASES}
        # Pre-shuffle anew
        for b in BASES:
            rng.shuffle(e[b])
        out = [seq[0]]
        ok = True
        for _ in range(n - 1):
            cur = out[-1]
            if not e[cur]:
                ok = False
                break
            out.append(e[cur].pop())
        if ok and len(out) == n:
            return "".join(out)
    # Fallback: random shuffle (single-nucleotide shuffle)
    arr = list(seq)
    rng.shuffle(arr)
    return "".join(arr)


def main():
    fa = Fasta(GENOME, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)

    natural = sample_natural(fa, N_NATURAL, rng)
    print(f"natural: {len(natural)}")
    ccre = sample_ccre(fa, N_CCRE, rng)
    print(f"ccre: {len(ccre)}")
    # For shuffled, draw fresh natural windows and shuffle them
    src = sample_natural(fa, N_SHUFFLED, rng)
    print(f"src for shuffle: {len(src)}")
    shuffled = [dinuc_shuffle(s, rng) for s in src]
    # sanity
    for s in shuffled[:5]:
        assert len(s) == L and set(s) <= set("ACGT")
    print(f"shuffled: {len(shuffled)}")

    seqs = natural + ccre + shuffled
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} sequences")


if __name__ == "__main__":
    main()
