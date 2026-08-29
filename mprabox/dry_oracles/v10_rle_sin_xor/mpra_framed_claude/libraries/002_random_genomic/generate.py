"""Experiment 002: random 200bp windows from hg38 autosomes.

Tests whether *natural* genomic sequence statistics (real motif occurrences,
realistic GC distribution, real co-occurrence patterns) lift held-out
correlations above the random-uniform-DNA floor — especially in SK-N-SH where
the baseline gave r≈0.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
REF = Path(__file__).resolve().parents[2] / "data" / "hg38.fa"


def main() -> None:
    fa = Fasta(str(REF))
    autosomes = [f"chr{i}" for i in range(1, 23)]
    chrom_lens = {c: len(fa[c]) for c in autosomes}
    total = sum(chrom_lens.values())
    weights = np.array([chrom_lens[c] / total for c in autosomes])

    rng = np.random.default_rng(SEED)
    seqs: list[str] = []
    attempts = 0
    while len(seqs) < N_SEQS:
        attempts += 1
        chrom = autosomes[rng.choice(len(autosomes), p=weights)]
        L = chrom_lens[chrom]
        start = int(rng.integers(0, L - SEQ_LEN))
        s = str(fa[chrom][start:start + SEQ_LEN]).upper()
        if "N" in s:
            continue
        seqs.append(s)

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    out = Path(__file__).parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences (attempts={attempts}) to {out}")


if __name__ == "__main__":
    main()
