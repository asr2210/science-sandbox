# 001_random_baseline

## Design
50,000 uniform random 200bp sequences from {A,C,G,T}. Single random seed (0).

## Hypothesis
Random sequences have no real regulatory motifs. A model trained on them
should perform near chance on natural regulatory eval sets, establishing
a floor of zero or near-zero predictive correlation.

## Result
- eval_01: mean_r = 0.2307 (K562=0.14, HepG2=-0.09, SKNSH=0.64)
- Most evals cluster around mean_r ≈ 0.22–0.23
- eval_08 stands out: mean_r = 0.089 (much lower)
- Runtime: 41s eval + ~30s setup

## Interpretation (surprising)
The "floor" is NOT zero. Random sequences yield mean_r ≈ 0.23.
Driver: SK-N-SH r=0.64 is remarkably high. K562 and HepG2 are near zero
(HepG2 slightly negative). The model trained on 50k random sequences
captures whatever compositional features (GC%, k-mer abundances,
poly-tracts) the MPRA assay responds to in SK-N-SH. SK-N-SH activity
appears to have substantial composition-driven variance that is
predictable from compositional features alone — which a model trained
on random sequences with measured outputs can learn.

eval_08 is structurally different from the others — its SK-N-SH r is
only 0.17, suggesting it filters or contrasts out the bulk
compositional signal. eval_08 may be a held-out set where simple
composition matters less (e.g., active vs. matched control comparison,
or variants-only).

Sets 02/05/14, 03/12, 04/09, 06/11 give nearly identical numbers —
likely correlated or replicate eval sets.

## Implications for theory
- Compositional features explain ~0.6 of SK-N-SH activity variance,
  ~0 of HepG2. Cell types differ in how much "non-grammar" signal
  exists.
- The challenge is HepG2 (and possibly K562) — these need real motif
  grammar to predict.
- eval_08 is the most discriminating set for "real" regulatory signal
  vs. composition. Watch it closely.
- A library that improves HepG2 r and eval_08 mean_r is more
  generalizable than one that only improves SK-N-SH.

## Next
Sample natural regulatory regions (ENCODE cCREs) across many cell types.
Expect: substantial lift on HepG2 and K562; eval_08 lift will be the
real signal of regulatory grammar learning.
