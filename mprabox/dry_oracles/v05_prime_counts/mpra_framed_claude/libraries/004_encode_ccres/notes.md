# Exp 004 — ENCODE cCRE-centered windows

## Design
50K x 200bp, centered on uniformly-sampled ENCODE V3 cCRE midpoints.
1.06M cCREs available; sampled 50,000. GC = 0.485 (cCREs are GC-rich).

## Result
**eval_01 = 0.0432. Essentially same as random hg38 (0.049) and random
uniform (0.042).**

Disappointingly flat. eval_08 = 0.066, eval_13 = 0.025.

## Interpretation
Major surprise. I predicted ≥0.15 eval_01; got 0.04. cCREs are the most
strongly enriched-for-regulatory-activity set you can get from public data,
yet the trained model is no better than from random sequences.

Working hypotheses for why:
1. **All-active library = no contrast.** If every sequence is high-activity,
   the model just learns "predict high". On a held-out test with mixed
   activity, predictions are uniformly high → low correlation.
2. **Eval sets test something orthogonal.** Maybe they include lots of
   non-regulatory or cell-type-specific sequences where cCRE knowledge
   doesn't transfer.
3. **Model bottleneck.** A from-scratch model trained on 50K seqs may
   simply not learn beyond shallow features (GC, k-mers) regardless of
   what's in the library — so library choice barely matters in this regime.

Important clue: **all libraries cluster at eval_01 ≈ 0.04–0.05** so far.
This is a strong floor that doesn't budge with realism, composition, or
regulatory enrichment alone. Whatever the unlock is, none of these hit it.

eval_08 ≈ 0.066 here, vs 0.124 for random uniform. Random uniform actually
wins eval_08, strengthening my prior that eval_08 rewards distributional
flatness, not biological signal.

## Next step
Try the opposite tack: deliberate **dynamic range across measured activity**.
Mix active (cCRE) with inactive (gene-desert random) sequences in equal
parts. Hypothesis: the model needs contrast between active and inactive
sequences to learn what features drive activity.

## Time
19.8s evaluator, ~50s wall.
