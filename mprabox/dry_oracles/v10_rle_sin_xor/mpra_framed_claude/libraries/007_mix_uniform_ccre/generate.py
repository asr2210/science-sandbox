"""Experiment 007: 50/50 mixture of random uniform + ENCODE cCREs.

25,000 random uniform 200bp + 25,000 stratified cCRE-centered 200bp (same
stratification across 8 ENCODE classes as exp 003). Shuffled together.

Tests if heterogeneous training data outperforms either pure component.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
N_RANDOM = N_SEQS // 2
N_CCRE = N_SEQS - N_RANDOM
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
REF = REPO / "data" / "hg38.fa"
BED = REPO / "data" / "cCREs_v4.bed"
AUTOSOMES = {f"chr{i}" for i in range(1, 23)}


def make_random(rng: np.random.Generator, n: int) -> list[str]:
    alphabet = np.array(["A", "C", "G", "T"])
    idx = rng.integers(0, 4, size=(n, SEQ_LEN), dtype=np.uint8)
    return ["".join(row) for row in alphabet[idx]]


def make_ccre(rng: np.random.Generator, n: int) -> list[str]:
    fa = Fasta(str(REF))
    by_type: dict[str, list[tuple[str, int, int]]] = {}
    with open(BED) as f:
        for line in f:
            chrom, start, end, _, _, ctype = line.rstrip().split("\t")[:6]
            if chrom not in AUTOSOMES:
                continue
            by_type.setdefault(ctype, []).append((chrom, int(start), int(end)))
    types = sorted(by_type.keys())
    per_type = n // len(types)
    remainder = n - per_type * len(types)

    seqs: list[str] = []
    for i, t in enumerate(types):
        k = per_type + (1 if i < remainder else 0)
        elems = by_type[t]
        idx = rng.choice(len(elems), size=k, replace=(k > len(elems)))
        for j in idx:
            chrom, s, e = elems[j]
            mid = (s + e) // 2
            st = mid - SEQ_LEN // 2
            en = st + SEQ_LEN
            if st < 0 or en > len(fa[chrom]):
                continue
            seq = str(fa[chrom][st:en]).upper()
            if "N" in seq or len(seq) != SEQ_LEN:
                continue
            seqs.append(seq)
    # top up if any rejected
    flat = [tup for v in by_type.values() for tup in v]
    while len(seqs) < n:
        chrom, s, e = flat[rng.integers(0, len(flat))]
        mid = (s + e) // 2
        st = mid - SEQ_LEN // 2
        en = st + SEQ_LEN
        if st < 0 or en > len(fa[chrom]):
            continue
        seq = str(fa[chrom][st:en]).upper()
        if "N" not in seq and len(seq) == SEQ_LEN:
            seqs.append(seq)
    return seqs[:n]


def main() -> None:
    rng = np.random.default_rng(SEED)
    rand_seqs = make_random(rng, N_RANDOM)
    ccre_seqs = make_ccre(rng, N_CCRE)
    seqs = rand_seqs + ccre_seqs
    rng.shuffle(seqs)
    seqs = seqs[:N_SEQS]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    gc_r = np.mean([(s.count("G") + s.count("C")) / SEQ_LEN for s in rand_seqs])
    gc_c = np.mean([(s.count("G") + s.count("C")) / SEQ_LEN for s in ccre_seqs])
    print(f"avg GC random={gc_r:.3f}  cCRE={gc_c:.3f}")
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
