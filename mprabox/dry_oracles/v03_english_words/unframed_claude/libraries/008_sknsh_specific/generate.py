"""Experiment 008: 50k real MPRA sequences that are most SKNSH-specific.

Hypothesis: K562/HepG2 r is limited by prediction *agreement*; SKNSH r by
prediction *variance*. Pick sequences whose SKNSH activity dominates K562/HepG2:
    score = |SKNSH_log2FC| - max(|K562_log2FC|, |HepG2_log2FC|)
Top 50k by this score. These sequences SHOULD: (a) trigger SKNSH-model variance,
(b) leave K562/HepG2 models in their "boring/baseline" regime where their two
variants agree closely, mimicking random uniform.

If both predictions hold, K562/HepG2 r approaches random-uniform levels and
SKNSH r climbs above 0.124 → first mean_r > 0.42.
"""
import os

SOURCE = "/tmp/mpra_data.txt"
N_SEQS = 50_000
LEN = 200


def main():
    records = []
    with open(SOURCE) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        ik, ih, isk, iseq = (
            header.index("K562_log2FC"),
            header.index("HepG2_log2FC"),
            header.index("SKNSH_log2FC"),
            header.index("sequence"),
        )
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= iseq:
                continue
            seq = parts[iseq].upper()
            if len(seq) != LEN or any(c not in "ACGT" for c in seq):
                continue
            try:
                k, h, s = abs(float(parts[ik])), abs(float(parts[ih])), abs(float(parts[isk]))
            except ValueError:
                continue
            score = s - max(k, h)
            records.append((score, seq))
    print(f"loaded {len(records)} sequences")
    records.sort(key=lambda x: -x[0])
    top = records[:N_SEQS]
    print(f"score top {N_SEQS}: max={top[0][0]:.3f}  min={top[-1][0]:.3f}")
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for _, s in top:
            f.write(s)
            f.write("\n")
    print(f"wrote {N_SEQS} SKNSH-specific sequences")


if __name__ == "__main__":
    main()
