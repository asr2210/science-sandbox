"""Experiment 006: top-50k real MPRA sequences by sum of absolute log2FC
across K562, HepG2, SKNSH.

Hypothesis: pushing real-sequence activity to its extreme should maximise
the prediction variance in EACH cell line — including SKNSH where variance
is the binding constraint — without falling out of the Malinois training
distribution. Predict that K562/HepG2 r recovers vs random while SKNSH r
climbs above 0.12.
"""
import os

SOURCE = "/tmp/mpra_data.txt"
N_SEQS = 50_000
LEN = 200


def main():
    records = []  # (score, sequence)
    with open(SOURCE) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        idx_k562 = header.index("K562_log2FC")
        idx_hepg2 = header.index("HepG2_log2FC")
        idx_sknsh = header.index("SKNSH_log2FC")
        idx_seq = header.index("sequence")
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= idx_seq:
                continue
            seq = parts[idx_seq].upper()
            if len(seq) != LEN or any(c not in "ACGT" for c in seq):
                continue
            try:
                k = abs(float(parts[idx_k562]))
                h = abs(float(parts[idx_hepg2]))
                s = abs(float(parts[idx_sknsh]))
            except ValueError:
                continue
            score = k + h + s
            records.append((score, seq))
    print(f"loaded {len(records)} scored sequences")
    records.sort(key=lambda x: -x[0])
    top = records[:N_SEQS]
    print(f"score range top {N_SEQS}: max={top[0][0]:.3f}, min={top[-1][0]:.3f}")
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as fout:
        for _, s in top:
            fout.write(s)
            fout.write("\n")
    print(f"wrote {N_SEQS} top-activity sequences")


if __name__ == "__main__":
    main()
