"""Experiment 020: JASPAR-PWM motif pool.

Parses JASPAR 2024 CORE vertebrate PFMs, builds PWMs (with pseudocount),
and for each of 50K seqs samples a uniformly-chosen motif and a sequence
from that motif's PWM, inserted at a random position.

This gives much larger motif diversity (~870 motifs) AND per-instance
variation (each motif instance differs because sampled from PWM).
"""
import os
import re
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 70
JASPAR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "..", "data", "jaspar2024_vert.txt"))


def parse_jaspar(path):
    """Return list of (name, pfm) where pfm is np array shape (4, L)."""
    motifs = []
    with open(path) as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(">"):
            name = line[1:].strip()
            rows = []
            for j in range(4):
                row_line = lines[i + 1 + j]
                # extract numbers between brackets
                m = re.search(r"\[(.*)\]", row_line)
                content = m.group(1) if m else row_line.split(None, 1)[1]
                nums = [float(x) for x in content.split()]
                rows.append(nums)
            pfm = np.array(rows, dtype=np.float64)
            motifs.append((name, pfm))
            i += 5
        else:
            i += 1
    return motifs


def pfm_to_probs(pfm, pseudo=1.0):
    """Convert PFM (counts) to PPM (probabilities)."""
    counts = pfm + pseudo
    return counts / counts.sum(axis=0, keepdims=True)


def main():
    rng = np.random.default_rng(SEED)
    motifs = parse_jaspar(JASPAR_PATH)
    # Filter to motifs with length 5-15 bp
    motifs = [(n, p) for n, p in motifs if 5 <= p.shape[1] <= 15]
    print(f"Loaded {len(motifs)} JASPAR motifs (length 5-15)")

    # Pre-compute probabilities and cumulatives per column for sampling
    motif_probs = [pfm_to_probs(p) for n, p in motifs]
    motif_cum = [np.cumsum(mp, axis=0) for mp in motif_probs]  # (4, L)
    motif_lens = np.array([mp.shape[1] for mp in motif_probs])

    bases = np.array(list("ACGT"))
    mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]

    m_idx_per_seq = rng.integers(0, len(motifs), size=N_SEQ)
    for i in range(N_SEQ):
        midx = m_idx_per_seq[i]
        mlen = motif_lens[midx]
        cum = motif_cum[midx]  # shape (4, mlen)
        # sample per-column
        u = rng.random(mlen)
        sampled_idx = (u[None, :] < cum).argmax(axis=0)  # shape (mlen,)
        pos = rng.integers(0, LEN - mlen + 1)
        mat[i, pos:pos + mlen] = bases[sampled_idx]

    with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
        f.write("\n".join("".join(row) for row in mat) + "\n")
    print(f"Wrote {N_SEQ} seqs; JASPAR PWM-sampled motif per seq")


if __name__ == "__main__":
    main()
