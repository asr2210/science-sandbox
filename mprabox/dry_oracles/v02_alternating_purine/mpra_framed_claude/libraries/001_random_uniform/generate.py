"""
Experiment 001 — baseline: pure uniform-random sequences.

Generates 50,000 sequences of length 200, each base sampled iid from
{A,C,G,T} with probability 0.25 each. Single random seed (0).

This is a control library — no regulatory grammar, no genomic structure,
no motifs. Establishes the floor for what a model can learn from
randomly assembled 200bp windows.
"""
import os
import numpy as np

N_SEQ = 50_000
L = 200
SEED = 0
BASES = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    # vectorized: generate all 50000 * 200 = 10M base indices at once
    idx = rng.integers(0, 4, size=(N_SEQ, L), dtype=np.uint8)
    chars = BASES[idx]
    with open(out_path, "w") as f:
        for row in chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    # sanity check
    with open(out_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == N_SEQ, f"expected {N_SEQ} lines, got {len(lines)}"
    assert all(len(s) == L for s in lines), "wrong length"
    assert all(set(s) <= set("ACGT") for s in lines[:1000]), "bad bases"
    print(f"wrote {len(lines)} sequences of length {L} to {out_path}")

if __name__ == "__main__":
    main()
