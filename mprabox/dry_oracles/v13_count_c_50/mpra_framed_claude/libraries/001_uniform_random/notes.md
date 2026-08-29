# Experiment 001 — Uniform random baseline

## Design
- 50,000 sequences of 200bp, each base i.i.d. uniform over {A,C,G,T}, seed=0
- Pure null. Establishes the floor: what a model can predict knowing nothing
  about real regulatory grammar.

## Results
mean_r summary (sorted high → low):
- eval_08: **0.5795**  (HepG2=0.76, SKNSH=0.80, K562=0.18 — huge cell asym.)
- eval_04: 0.3902      (K562 0.33, HepG2 0.36, SKNSH 0.49)
- eval_09: 0.3902      (identical to eval_04 — possible duplicate)
- eval_01: 0.1294  ← primary
- eval_14: 0.1294      (== eval_01)
- eval_02: 0.1281
- eval_05: 0.1281      (== eval_02)
- eval_06: 0.1189
- eval_11: 0.1189      (== eval_06)
- eval_10: 0.0938
- eval_03: 0.0771
- eval_12: 0.0771      (== eval_03)
- eval_07: -0.1416
- eval_13: -0.1470     (~ eval_07)

Total: 48s (eval portion 19s). Very fast — leaves headroom for many experiments.

## Key observations
1. **Eval duplication**: eval pairs are identical or near-identical:
   (01,14), (02,05), (03,12), (06,11), (04,09), (07,13). eval_08 unique.
   Effective number of independent evals ≈ 7–8.
2. **eval_08 dominated by composition**: random sequences reach r=0.58 with
   only base-frequency signal. Suggests eval_08 measures something heavily
   determined by simple compositional features (GC, dinucleotides, length-200
   global stats). HepG2/SKNSH carry it; K562 is low (0.18).
3. **eval_07/13 negative**: random library *anti-correlates* with HepG2 and
   SKNSH in these sets. Likely a set where active sequences are
   compositionally distinct from random and the model fits the wrong gradient.
4. **K562 consistently ~0.20–0.33 across nearly all evals** — K562 readouts
   may be easier or more compositionally-driven than HepG2/SKNSH.
5. **eval_01 (primary) = 0.13** — solid baseline floor to beat.

## What this means for theory
The library teaches the model *something* even when the sequences are
i.i.d. random, because the MPRA readouts themselves have compositional
dependencies (GC, dinucleotide frequency, k-mer effects on transcription).
This is the absolute floor: ~0.13 on eval_01.

The asymmetry across eval sets is the most interesting signal: some evals
appear nearly fully explainable by composition (eval_08), others actively
penalize a pure-composition prior (eval_07/13). The library needs to teach
the model *both* compositional and grammatical features to do well across
the full evaluation panel.

## Next experiment idea
Compare to natural genomic sequences. If random hits 0.13 and natural hits
0.30+, that quantifies the value of real motif context. Use random hg38
regions or shuffle composition-matched controls.
