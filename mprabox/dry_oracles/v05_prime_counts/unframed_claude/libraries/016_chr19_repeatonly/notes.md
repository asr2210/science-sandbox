# Experiment 016 — chr19 REPEAT-ONLY windows

## Hypothesis
Counter-hypothesis: if non-repeat hurt eval_01, maybe pure repeat
sequences are the source of signal.

## Method
Keep only chr19 windows that are 100% LOWERCASE soft-masked
(repeats: LINE/SINE/Alu/etc).

## Results — NEW BEST on eval_01
- eval_01: 0.0518 (chr19: 0.0502, non-repeat: 0.0358) → ✓ NEW BEST
- eval_04, eval_09: 0.0581 each (chr19: 0.057)
- avg: ~0.048

## Interpretation
Confirms T9: repeat sequence is the primary source of eval_01
signal in chr19. Removing repeats lost 30% of the signal. Keeping
only repeats GAINED a small amount over the natural chr19 mix.

But gain is small (+0.0016). The lever is "repeat-like sequence
content" but not dramatically beyond plain chr19.

## Theory update — T10
Repeat-rich DNA gives the best eval_01. Possible reasons:
1. Repeats have characteristic k-mer spectra both scoring axes
   recognize as "DNA-like"
2. Repeats contain TFBS/regulatory motifs (Alu-derived enhancers)
3. The oracle was trained on data where repeat content was a
   strong predictor

Step-function still elusive. Maybe ALU specifically (most common
repeat, ~10% of genome, harbors many TFBSs) is the key vs mixed
repeat types (LINE which dominates by mass).

## Next
EXP 17: synthetic Alu-derived sequences. Use AluY consensus
~300bp, take 200bp segments, mutate at low rate. Tests whether
ALU is the specific repeat class driving the signal.
