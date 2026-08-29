"""013_malinois_active: 50k Malinois oligos selected for high measured activity.

Exp 012 (random Malinois subsample) gave 0.6856 — slightly below cCREs
because most Malinois oligos are random genomic backgrounds around
variants, with little regulatory signal. The hypothesis here is that
the *highly-active subset* (large |log2FC| in any cell type) should be
much more informative: those sequences contain detectable motif
arrangements that drive measurable activity.

Selection: rank oligos by max(|K562_log2FC|, |HepG2_log2FC|,
|SKNSH_log2FC|), take the top 50k. This picks sequences with strong
positive (activator) OR strong negative (silencer) effects in any
labeled cell type. Both teach the model something — net of motif
weights / silencer marks.

Generalization rationale: Highly-active sequences contain the
strongest, most repeated regulatory motifs. Those motifs are likely
conserved across cell types and the underlying grammar should
generalize to unseen cell types that share those TFs / chromatin
contexts. Sequences with near-zero activity in the labeled cell types
might be irrelevant decoys (chromatin-closed, no TFs available there),
not informative non-regulatory examples.

Risk: selecting only highly-active may starve the model of
realistic-distribution training data, biasing it to predict high
activity always. We'll see if eval_01 reflects that.
"""
import os

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 13


def load_seqs_with_activity(path):
    seqs = []; mags = []
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
            mag = max(abs(k), abs(h), abs(n))
            seqs.append(s); mags.append(mag)
    return seqs, np.array(mags)


def main():
    seqs, mags = load_seqs_with_activity(MPRA_PATH)
    print(f"  loaded {len(seqs)} 200bp ACGT sequences with activity", flush=True)
    # Top-N by max abs log2FC across cell types
    top_idx = np.argpartition(-mags, N)[:N]
    print(f"  selected top {N}, max|log2FC| threshold = {mags[top_idx].min():.3f}", flush=True)
    rng = np.random.default_rng(RNG_SEED)
    order = rng.permutation(len(top_idx))
    picked = [seqs[top_idx[i]] for i in order]
    with open(OUT_PATH, "w") as f:
        for s in picked:
            f.write(s); f.write("\n")
    print(f"Wrote {len(picked)} sequences", flush=True)


if __name__ == "__main__":
    main()
