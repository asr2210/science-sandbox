# Exp 002 — 1st-order Markov (dinucleotide-matched)

## Design
50K x 200bp sampled from 1st-order Markov chain with hand-curated human-genome
transition probabilities (~41% GC stationary, CpG depletion 5x). First base
sampled from stationary distribution.

Empirical: GC = 0.462 (target 0.41 — my matrix isn't perfectly stationary;
ended up GC-richer than intended), CpG fraction = 0.009 (target ~0.01,
matches genome).

## Result
**eval_01 = 0.0094, mean = 0.014. Worse than uniform random (0.042).**

Most surprising: **HepG2 is negative across all 14 evals** (~-0.04). K562 and
SK-N-SH are slightly positive.

eval_08 dropped from 0.124 (random uniform) to 0.066.

## Interpretation
This contradicted my expectation. I expected dinuc-matched to be a *better*
baseline; instead it's worse. Hypotheses:

1. **GC drift hurt me**: my first base from PI=41% GC but chain converges
   higher (46%). This may have shifted the per-sequence GC distribution in
   ways the model picked up wrongly.
2. **Negative HepG2** suggests the model learned a feature (probably global
   GC) that anti-predicts HepG2 activity from compositional cues alone.
   HepG2 enhancers may favor different GC than K562/SK-N-SH.
3. **eval_08 drop** is consistent: uniform random has flatter composition; my
   dinuc library introduced *non-genomic* CG depletion that doesn't match
   what eval_08 cares about (or eval_08 cares about something other than
   k-mer composition entirely).

Big lesson: **introducing composition without motifs can be net-harmful** —
the model learns the wrong features and uses them incorrectly. "Realistic
baseline" is not necessarily a better baseline.

## Time
13.2s evaluator, ~50s wall.
