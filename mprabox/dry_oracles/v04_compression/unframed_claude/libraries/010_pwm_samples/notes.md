# 010 — PWM-sampled fuzzy motifs (3/seq, 17 TFs) — BREAKTHROUGH

## Hypothesis
PWM sampling produces FUZZY realistic motifs (different sequence each draw)
that might be recognized where rigid consensus strings (exp 003) were not.

## Setup
17 well-known human TFs from JASPAR2024 CORE (SP1, MYC, MAX, USF1/2, CREB1,
JUN, FOS, NFYA/B, GATA1/2, ELF1, ELK1, ETS1, KLF4, EGR1).
Each 200bp sequence: uniform random base, 3 PWM-sampled motifs inserted at
random positions, 50% RC.

## Results
eval_01 = **0.3644** (random 0.3157, **+0.049**).
Big wins on eval_04 (+0.09), eval_10 (+0.06). Loss on eval_07 (-0.05).
Most evals UP.

## Key insight
The lever is PWM SAMPLING, not consensus strings. The predictor recognizes
FUZZY PWM-shaped content (like real ChIP-seq peaks would have), not
hardcoded canonical motifs. This matches the bio of trained MPRA models.

## Skills produced
- Use pyjaspar / JASPAR2024 to sample PWM realizations.

## Next
- 011: same 17 TFs but 6 motifs/seq → does density help further?
- 012: all 720 human PWMs, 6 motifs/seq → does TF diversity help?
