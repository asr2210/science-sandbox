"""
Experiment 003: ENCODE cCRE-enriched library.

Sample 50,000 ENCODE candidate cis-regulatory elements (V3 combined,
ENCODE3, 926k elements across hg38 primary chromosomes). For each
sampled cCRE, extract a 200bp window centered on the cCRE midpoint.

Hypothesis: a library enriched in regulatory elements has much higher
signal-to-noise than random genomic windows because every sequence
contains a TFBS/motif structure that drives measurable activity. This
should give the model a denser training signal for motif → activity
mapping.

Predictions vs exp 002 (random genomic, mean_r=0.458):
- eval_01 should rise from 0.50 to 0.55–0.65 (PRIMARY)
- eval_07/13 should rise from 0.62 to 0.70+ (motif-grounded evals)
- eval_08 may stay negative or worsen (cCREs are *more* "natural"
  than random genomic, so the eval_08 inversion may deepen)
- eval_04/09 likely unchanged (composition-axis)

Generalization argument: cCREs are an ENCODE-wide regulatory catalog
drawn from chromatin signatures in MANY cell types (not just K562/
HepG2/SK-N-SH). So the library covers regulatory grammar from across
the cell-type spectrum and should train a model that generalizes to
unseen cell types more than a library hand-picked for our three.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FA_PATH = os.path.join(ROOT, "data", "hg38.fa")
BED_PATH = os.path.join(ROOT, "data", "cCRE_v3_primary.bed")

COMP = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N",
        "a": "t", "t": "a", "g": "c", "c": "g", "n": "n"}

def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)

    # Load cCREs: chr, start, end, name, label
    cres = []
    with open(BED_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            start = int(parts[1])
            end = int(parts[2])
            cres.append((chrom, start, end))
    print(f"loaded {len(cres)} cCREs")

    # Shuffle and iterate; reject windows with N, off-end, or already too short
    idx_order = rng.permutation(len(cres))
    seqs = []
    attempts = 0
    chrom_len = {c: len(fa[c]) for c in {x[0] for x in cres}}
    for i in idx_order:
        attempts += 1
        chrom, s, e = cres[int(i)]
        mid = (s + e) // 2
        ws = mid - L // 2
        we = ws + L
        if ws < 0 or we > chrom_len[chrom]:
            continue
        seq = str(fa[chrom][ws:we]).upper()
        if "N" in seq:
            continue
        if rng.random() < 0.5:
            seq = revcomp(seq)
        seqs.append(seq)
        if len(seqs) == N:
            break

    if len(seqs) != N:
        raise RuntimeError(f"only got {len(seqs)} sequences after {attempts} attempts")

    with open(OUT, "w") as f:
        f.write("\n".join(seqs) + "\n")

    # Verify
    with open(OUT) as f:
        lines = f.read().splitlines()
    assert len(lines) == N
    for i, l in enumerate(lines[:5]):
        assert len(l) == L
        assert set(l) <= set("ACGT")
    print(f"wrote {len(lines)} cCRE-centered sequences (rejection {1 - N/attempts:.2%})")

if __name__ == "__main__":
    main()
