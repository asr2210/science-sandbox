"""Experiment 009: alphabet cyclic permutation of exp 001 sequences.

Test if the score depends on specific base identities (alphabet asymmetry).
Take exp 001 sequences and relabel: 0->1, 1->2, 2->3, 3->0.
"""
import os

PERM = {"0": "1", "1": "2", "2": "3", "3": "0"}

def main():
    here = os.path.dirname(__file__)
    src = os.path.join(here, "..", "001_uniform_random", "sequences_0.txt")
    with open(src) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    assert len(lines) == 50_000
    relabeled = [line.translate(str.maketrans(PERM)) for line in lines]
    out = os.path.join(here, "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(relabeled) + "\n")
    print(f"wrote {len(relabeled)} relabeled sequences to {out}")
    print("orig[0][:30]:", lines[0][:30])
    print("relabel[0][:30]:", relabeled[0][:30])

if __name__ == "__main__":
    main()
