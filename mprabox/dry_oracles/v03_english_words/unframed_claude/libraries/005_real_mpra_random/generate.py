"""Experiment 005: 50k real MPRA sequences randomly sampled from the Malinois
training dataset (Gosai et al., Nature 2024).

Hypothesis: the eval metric is correlation between two Malinois-derived
scoring functions on YOUR library. Real MPRA sequences are in-distribution
for both models, so their predictions should agree more strongly than on
random sequences. Should beat random-uniform (eval_01 = 0.4200).

Data source: gs://tewhey-public-data/CODA_resources/Table_S2__MPRA_dataset.txt
(downloaded to data/mpra_table_s2.txt; also kept at /tmp/mpra_data.txt)
"""
import os
import random

SOURCE = "/tmp/mpra_data.txt"
N_SEQS = 50_000
LEN = 200
RNG_SEED = 1005


def main():
    seqs = []
    # column 12 (1-based) = "sequence"
    with open(SOURCE) as fh:
        header = fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 12:
                continue
            seq = parts[11].upper()
            if len(seq) != LEN:
                continue
            if any(c not in "ACGT" for c in seq):
                continue
            seqs.append(seq)
    print(f"loaded {len(seqs)} clean 200bp sequences from MPRA Table S2")
    rng = random.Random(RNG_SEED)
    chosen = rng.sample(seqs, N_SEQS)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as fout:
        fout.write("\n".join(chosen))
        fout.write("\n")
    print(f"wrote {N_SEQS} sequences to {out_path}")


if __name__ == "__main__":
    main()
