# 001_random_uniform — notes

## Design
50,000 sequences of 200bp, each base drawn IID uniform from {A,C,G,T}, seed 0.
Pure-random baseline. No regulatory grammar, no motif, no GC bias.

## Generalization argument
This library would be terrible for predicting expression in unseen cell types
because the model can only learn base-composition effects (GC content, dinucleotide
preferences) that emerge by chance from 200bp windows. Any predictive ability is a
floor for what an MPRA library can achieve.

## Result (56s, then 88s wall)
- eval_01: 0.3068  (primary)
- range: 0.110 (eval_08) to 0.402 (eval_07)
- mean_r overall ≈ 0.30

## Observations
1. K562 == HepG2 in every eval, exactly. Either the model output collapses to
   K562=HepG2 for random DNA (no cell-type-specific signal to learn) or these
   two cell types share the same labels in the eval set. Will check with a real
   library next.
2. Several evals are *identical* (eval_01==eval_05==eval_14; eval_03==eval_12;
   eval_04==eval_09; eval_06==eval_11). So there are ~9 distinct eval sets.
3. eval_07 easiest (0.40), eval_08 hardest (0.11). The hardest set might be the
   most genuinely "out of distribution".
4. r=0.30 from pure random DNA is surprisingly high — must be GC/composition.

## Update to theory
Composition alone gives r≈0.30 → real libraries need to beat this clearly. The
~3x gap from 0.30 to the implied ceiling (1.0) is the room to improve via
regulatory grammar.
