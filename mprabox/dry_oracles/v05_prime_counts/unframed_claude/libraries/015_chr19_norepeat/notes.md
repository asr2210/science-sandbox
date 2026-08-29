# Experiment 015 — chr19 NON-REPEAT windows

## Hypothesis
Removing repeat sequences (LINE/SINE/Alu) leaves "informative"
functional DNA, which should boost r above plain chr19 (0.050).

## Method
Keep only 200bp windows that are 100% UPPERCASE ACGT in
soft-masked chr19.fa (~17% of windows pass).

## Results
- eval_01: 0.0358 (chr19: 0.0502) → MUCH WORSE
- eval_08: 0.0581 (chr19: 0.0551) → slightly BETTER
- avg: ~0.034

## Interpretation
HYPOTHESIS REJECTED. Removing repeats HURT eval_01 by 30%. The
soft-masked repetitive sequence in chr19 (Alu, LINE, SINE) is
actually CONTRIBUTING the signal for eval_01.

This is opposite of expected. Possibilities:
- Repeats provide compositional diversity the metric tracks
- Repeat content has motif-like patterns that correlate across axes
- Non-repeat is more GC-uniform/promoter-like — narrower variance

## Theory update — T9
Repeat sequence is part of the signal on eval_01. The mix of
repeat + non-repeat is what gives chr19 its 0.050. Pure non-repeat
loses signal; possibly pure repeat would too (need bimodal mix).

## Next
EXP 16: chr19 REPEATS ONLY (all-lowercase soft-masked windows).
If repeat-only gives high r → repeats ARE the signal.
If repeat-only gives low r → both classes needed, mix is key.
