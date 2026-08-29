"""Experiment 003: 200bp windows centered on ENCODE v4 cCREs (stratified).

50,000 windows drawn equally from the 8 cCRE annotation classes
(dELS, pELS, CA, CA-CTCF, TF, CA-H3K4me3, PLS, CA-TF) so the library has
balanced exposure to all regulatory categories — not weighted toward dELS
(which dominates the registry by count). 200bp centered on each cCRE midpoint
(padding into flanking genomic context where cCRE is shorter than 200bp).
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
REF = REPO / "data" / "hg38.fa"
BED = REPO / "data" / "cCREs_v4.bed"

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}


def main() -> None:
    fa = Fasta(str(REF))

    # Group cCREs by type, restricted to autosomes.
    by_type: dict[str, list[tuple[str, int, int]]] = {}
    with open(BED) as f:
        for line in f:
            chrom, start, end, _, _, ctype = line.rstrip().split("\t")[:6]
            if chrom not in AUTOSOMES:
                continue
            by_type.setdefault(ctype, []).append((chrom, int(start), int(end)))
    print({k: len(v) for k, v in by_type.items()})

    rng = np.random.default_rng(SEED)
    types = sorted(by_type.keys())
    per_type = N_SEQS // len(types)
    remainder = N_SEQS - per_type * len(types)

    seqs: list[str] = []
    for i, t in enumerate(types):
        n = per_type + (1 if i < remainder else 0)
        elems = by_type[t]
        idx = rng.choice(len(elems), size=n, replace=(n > len(elems)))
        got = 0
        attempted = 0
        for j in idx:
            attempted += 1
            chrom, s, e = elems[j]
            mid = (s + e) // 2
            start = mid - SEQ_LEN // 2
            end = start + SEQ_LEN
            if start < 0 or end > len(fa[chrom]):
                continue
            seq = str(fa[chrom][start:end]).upper()
            if "N" in seq or len(seq) != SEQ_LEN:
                continue
            seqs.append(seq)
            got += 1
        print(f"{t}: requested {n}, kept {got}")

    # Make up any shortfall with extra random cCREs from any class.
    flat = [tup for v in by_type.values() for tup in v]
    while len(seqs) < N_SEQS:
        chrom, s, e = flat[rng.integers(0, len(flat))]
        mid = (s + e) // 2
        start = mid - SEQ_LEN // 2
        end = start + SEQ_LEN
        if start < 0 or end > len(fa[chrom]):
            continue
        seq = str(fa[chrom][start:end]).upper()
        if "N" not in seq and len(seq) == SEQ_LEN:
            seqs.append(seq)

    # Shuffle so the model doesn't see them grouped by type during training.
    rng.shuffle(seqs)
    seqs = seqs[:N_SEQS]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
