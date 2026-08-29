# Experiment 006 — Real chr22 200bp windows

## Hypothesis
T3 said the model was trained on synthetic random. But the small
chr22→random gap could go either way. Decisive test: sample real
human genomic windows.

## Method
hg38 chr22 (50.8 Mb). Sample 50K random 200bp windows, reject any
window containing N. Seed=6.

## Results
- eval_01: 0.0492 (random uniform: 0.0420)  → SLIGHTLY HIGHER ✓
- eval_02: 0.0490 (0.0422)
- eval_03: 0.0479 (0.0413)
- eval_04: 0.0565 (0.0489)
- eval_07: 0.0305 (0.0254)
- eval_08: 0.0592 (0.1237)  → MUCH LOWER ✗
- eval_13: 0.0316 (0.0203)
- Average: ~0.046 (random: 0.046) — wash overall

## Interpretation
Real human DNA is slightly better than random uniform on most
evals (modest +0.005 to +0.010) but dramatically WORSE on eval_08.
The two distributions are roughly comparable on average.

**Important**: eval_01 (the primary metric) improved. This is a
real signal that natural DNA helps for eval_01 specifically.

eval_08 is a strange outlier — it loves uniform random and dislikes
natural DNA. Possibly its underlying model uses a simple feature
(e.g., k-mer entropy) that random uniform maximizes.

## Theory update — T4
T3 is partially wrong. Different evaluators in the suite prefer
different sequence distributions:
- eval_08 ("entropy-loving"): uniform random is best
- Most others: real natural is marginally better
- eval_01 (primary): real natural is marginally better

T4: the lever for the PRIMARY metric is sequence properties that
exist in real DNA but not synthetic random. Could be:
- Motif content (but cocktail didn't help → maybe wrong motifs)
- Real regulatory grammar
- CpG islands / gene-dense regions
- Repeats (Alus contain regulatory potential)
- GC content VARIANCE across the library (chr22 has wide GC range)

## Next
EXP 7: variable GC random library — each sequence has its own GC
drawn from Uniform[0.2, 0.8]. Tests if compositional variance
across the library is the lever, even without natural motif content.
