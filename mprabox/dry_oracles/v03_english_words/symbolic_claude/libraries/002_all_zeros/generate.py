"""Experiment 002: 50K identical all-zero sequences.

Probe: does the metric tolerate homogeneity, and is character '0'
favored or penalized? If the metric is Pearson r based, identical
sequences should yield NaN/0 (no variance in predictions).
If averaged per-sequence, we get the score of a constant-0 sequence.
"""
import os

N_SEQS = 50_000
SEQ_LEN = 200


def main():
    seq = "0" * SEQ_LEN
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for _ in range(N_SEQS):
            f.write(seq + "\n")
    print(f"Wrote {N_SEQS} sequences to {out_path}")


if __name__ == "__main__":
    main()
