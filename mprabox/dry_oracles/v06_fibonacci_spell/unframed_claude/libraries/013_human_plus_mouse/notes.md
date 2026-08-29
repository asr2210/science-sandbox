# Experiment 013: 25k hg38 + 25k mm10 chr1 (cross-species)

## Plan
Test cross-species hypothesis: mouse adds informative diversity beyond human.

## Result
- eval_01 mean_r = **0.1360** — WORSE than pure hg38 (0.1387)
- Mouse seqs dilute the hg38 distribution

## Implication
Mouse adds noise from the model's perspective (the test set is human MPRA;
mouse sequences carry "off-distribution" content that doesn't teach the
model human-relevant features).

T10 reinforced: distribution-matched, human-only, broadly sampled = best.

## Next
Need to check whether 0.1387 is near a ceiling or just one noisy sample.
Rerun hg38 random with a different seed and compare. If 0.139 ± 0.001,
I'm near ceiling. If wider, there's still room to optimize via sampling.
