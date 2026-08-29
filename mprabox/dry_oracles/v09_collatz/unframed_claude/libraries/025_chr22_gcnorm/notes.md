# Exp 025 — chr22 + gentle GC normalization — TOTAL DISASTER

50k chr22 tiles. For tiles with GC outside [45,53]%, gently flip
A↔G or T↔C until GC is near 49%. 68% of tiles modified, mean 15
flips per modified seq.

## Result — CATASTROPHIC

| metric  | chr22 random | + GC normalization |
|---------|-------------:|-------------------:|
| eval_01 | 0.3202       | **-0.0170**        |
| k562    | 0.1443       | -0.0469            |
| hepg2   | 0.1990       | -0.0886            |
| sknsh   | 0.6173       | 0.0844             |

ALL THREE cell types crashed massively. Even tiny base edits (15
of 200 bases = 7.5%) destroy the score completely.

**Theory v8 (HUGE)**: The scorer is extremely sensitive to sequence
"naturalness". Even moderate edits to real DNA produce sequences
that fall completely OUT OF DISTRIBUTION. The model can detect
edited-vs-natural sequences at a deep level — probably k-mer
distributions, dinucleotide context-dependent biases, or
positional motif statistics.

**STRICT IMPLICATION**: NEVER mutate, augment, splice, or otherwise
modify real DNA sequences. Use them EXACTLY as found in the
reference genome. Any composition tweak destroys score.

This rules out essentially all "engineering" strategies. Remaining
levers: WHICH natural sequences (which chromosome, which window
selection) to include.
