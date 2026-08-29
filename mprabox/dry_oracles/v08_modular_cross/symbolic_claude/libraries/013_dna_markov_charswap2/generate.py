"""Experiment 013: Different char swap (0↔2, 1↔3) on exp 9 sequences.

This swap CROSSES the {0,1}/{2,3} grouping (now {0,2} and {1,3}). If exp 12's
invariance was due to the specific {0,1} vs {2,3} grouping, this should give
different results. If results identical, the predictor is fully permutation
invariant.
"""
import os

src = os.path.join(os.path.dirname(__file__), "..", "009_dna_markov", "sequences_0.txt")
with open(src) as f:
    lines = [ln for ln in f.read().splitlines() if ln]
assert len(lines) == 50_000

mapping = str.maketrans("0123", "2301")  # 0->2, 1->3, 2->0, 3->1
mapped = [ln.translate(mapping) for ln in lines]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(mapped) + "\n")

print(f"Applied swap (0->2,1->3,2->0,3->1) to {len(mapped)} sequences")
