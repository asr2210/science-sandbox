"""015_malinois_cell_type_specific: 50k Malinois oligos with high cross-CT variance.

Exp 013 taught me that selecting on activity *magnitude* destroys the
training distribution. But selecting on activity *specificity* (how
different the cell types are from each other) is a different lever:
sequences with high between-CT std contain the discriminative signal
the model needs to distinguish K562/HepG2/SKNSH. Their absolute
activity can be moderate; they're not a magnitude tail.

Selection: top 50k oligos by std([K562_log2FC, HepG2_log2FC,
SKNSH_log2FC]) — i.e., the most cell-type-specific oligos.

Hypothesis: cell-type-specific sequences carry the per-CT TF grammar
that distinguishes the labels. Generic active sequences (high in all
CTs) teach generic motifs but not the discriminator. cCRE library
contains a natural mix of both; a CT-specific subset of Malinois
should be enriched for the discriminator signal.

Generalization concern: this is *still* selecting on the labels, just
on a derived quantity. If across-CT std distribution differs from the
eval set distribution, calibration could suffer. Risk noted.

Pre-flight check from exp 013: distribution-mismatch killed eval_01.
Mitigation: select on std (which is bounded ~0–3 in this data, much
more compact than max|log2FC|) and shuffle randomly to avoid further
bias.
"""
import os

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 15


def load_seqs_with_specificity(path):
    seqs = []; spec = []
    with open(path) as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            s = parts[11]
            if len(s) != L:
                continue
            if any(c not in "ACGT" for c in s):
                continue
            try:
                k = float(parts[5]); h = float(parts[6]); n = float(parts[7])
            except ValueError:
                continue
            arr = np.array([k, h, n])
            spec.append(arr.std())
            seqs.append(s)
    return seqs, np.array(spec)


def main():
    seqs, spec = load_seqs_with_specificity(MPRA_PATH)
    print(f"  loaded {len(seqs)} 200bp ACGT seqs w/ measurements", flush=True)
    top_idx = np.argpartition(-spec, N)[:N]
    print(f"  selected top {N} by cross-CT std; threshold = {spec[top_idx].min():.3f}", flush=True)
    rng = np.random.default_rng(RNG_SEED)
    order = rng.permutation(len(top_idx))
    picked = [seqs[top_idx[i]] for i in order]
    with open(OUT_PATH, "w") as f:
        for s in picked:
            f.write(s); f.write("\n")
    print(f"Wrote {len(picked)} sequences", flush=True)


if __name__ == "__main__":
    main()
