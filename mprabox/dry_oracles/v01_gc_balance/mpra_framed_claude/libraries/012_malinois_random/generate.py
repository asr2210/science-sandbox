"""012_malinois_random: 50k uniform-random subsample of Malinois MPRA oligos.

The Malinois dataset (Gosai et al. 2024 / Tewhey lab) contains 798k 200bp
MPRA oligos measured in K562, HepG2, and SK-N-SH — the same three cell
types my model will predict for. 763k of those oligos are exactly 200bp;
they tile real human regulatory variants from GTEX eQTLs and UKBB GWAS
loci, plus a smaller pool of cCRE-derived sequences.

Hypothesis: training sequences that were *explicitly designed to be
informative for K562/HepG2/SKNSH activity* should beat generic regulatory
sequence pools like cCREs. cCREs were selected for any-cell-type
regulatory potential; Malinois oligos were selected because variants in
them affect activity in these three cell types. That selection should
carry stronger signal for these cell types.

Generalization caveat: Malinois is biased toward variant-containing
sequences in two specific contexts (GTEX eQTL, UKBB GWAS). It may
under-represent some classes of regulatory grammar (CTCF boundaries,
strong promoters, polycomb-repressed regions). The model trained on it
might generalize less to those classes. We accept this tradeoff to test
the magnitude of the "real measured MPRA sequences" lever.
"""
import os

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 12


def load_seqs(path):
    seqs = []
    with open(path) as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            s = parts[11]
            if len(s) != L:
                continue
            if any(c not in "ACGT" for c in s):
                continue
            seqs.append(s)
    return seqs


def main():
    seqs = load_seqs(MPRA_PATH)
    print(f"  loaded {len(seqs)} 200bp ACGT sequences", flush=True)
    rng = np.random.default_rng(RNG_SEED)
    idx = rng.choice(len(seqs), size=N, replace=False)
    picked = [seqs[i] for i in idx]
    rng.shuffle(picked)
    with open(OUT_PATH, "w") as f:
        for s in picked:
            f.write(s); f.write("\n")
    print(f"Wrote {len(picked)} sequences", flush=True)


if __name__ == "__main__":
    main()
