# 004 — High-density motif packing

## Hypothesis
If motif content is the lever, packing ~20+ motifs per sequence (covering most
of the 200bp) should improve the score over sparse motifs and random.

## Results
eval_01 = **0.1660** (random=0.3157, sparse-motifs=0.3205). Big DROP.
eval_07 = 0.2370 (random 0.4481). Big drop.
eval_08 = 0.0241 (random 0.1032). Drop.
All evals dropped sharply.

## Key observations
This is the SECOND time a transformation that REDUCES library diversity
(GC60 in exp 002, motif-packing here) tanks the score. Both libraries are
internally repetitive: GC60 has every position skewed the same way, and
dense-motifs has every sequence built from the same 18-element vocabulary.

Random uniform DNA wins because its 50k sequences are maximally diverse:
each k-mer occurs at roughly its expected random frequency.

## Update to theory v4
The metric strongly rewards LIBRARY-LEVEL DIVERSITY of sequence statistics,
not per-sequence motif richness. Two non-mutually-exclusive interpretations:
(A) The metric is a correlation that requires variance in predicted activity
    across the 50k library. Homogeneous libraries → low variance → low r.
(B) The metric scores how well our 50k sequences span the model's input
    manifold — diverse libraries explore more "test cases."

## Next
Experiment 005: per-sequence GC sampled uniformly from [0.2, 0.8].
- If score > 0.32 → metric loves library variance (theory A).
- If score < 0.32 → metric rewards specifically "genome-like" composition.
- If ~0.32 → composition alone is irrelevant.

This is a single cheap dial that should disambiguate.
