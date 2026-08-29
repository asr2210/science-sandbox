"""Experiment 012: Char identity swap on exp 9 sequences.

Apply mapping 0↔1, 2↔3 to all chars of exp 9 sequences. Same dinucleotide
structure (after relabeling), different surface labels.

If results identical → predictor is invariant to char identity, only structure
matters. If results differ → predictor uses specific char identities.
"""
import os

src = os.path.join(os.path.dirname(__file__), "..", "009_dna_markov", "sequences_0.txt")
with open(src) as f:
    lines = [ln for ln in f.read().splitlines() if ln]
assert len(lines) == 50_000

mapping = str.maketrans("0123", "1032")
mapped = [ln.translate(mapping) for ln in lines]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(mapped) + "\n")

print(f"Swapped chars (0↔1, 2↔3) in {len(mapped)} sequences")
