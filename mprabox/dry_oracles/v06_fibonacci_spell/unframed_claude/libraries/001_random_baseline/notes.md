# Experiment 001: Random uniform baseline

## Plan
50,000 sequences of 200bp, each base uniform from {A,C,G,T}, seed=0.
Calibrates the scoring floor.

## Result
- eval_01 mean_r = 0.1176 (K562=0.012, HepG2=0.152, SKNSH=0.189)
- All evals span 0.057–0.122 mean_r
- eval_08 is markedly lower (0.0563) than the rest — different/stricter model

## Observations
1. **K562 is nearly uncorrelated** (~0.01) with random sequences. This cell type
   requires specific motifs/structure to trigger predicted activity. HepG2 and
   especially SK-N-SH respond to generic random sequences.
2. **Some evals are identical or near-identical**:
   - eval_02 == eval_05 (exactly identical numbers)
   - eval_04 == eval_09 (exactly identical)
   - eval_06 == eval_11 (exactly identical)
   - eval_03 == eval_12 (exactly identical)
   - eval_14 ≈ eval_01
   So there are effectively ~7–8 distinct test sets, not 14.
3. The scoring is consistent within an eval — small variance across cell types
   within an eval makes mean_r a reasonable summary.

## What this means for theory
T0 (regulatory motifs drive higher scores) is consistent: random gives a floor
but not zero. The non-zero baseline for HepG2/SKNSH suggests these cell-type
models also pick up GC/AT structural cues.

## Next step
Test whether GC content alone moves the score, isolating it from motif effects.
