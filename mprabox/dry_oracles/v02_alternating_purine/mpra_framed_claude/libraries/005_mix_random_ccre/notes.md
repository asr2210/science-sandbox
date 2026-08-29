# Experiment 005 — 50/50 mix: random genomic + genome-wide cCRE

## Design
- 25,000 random 200bp windows (genome-wide, length-weighted chromosome
  sampling; N-windows skipped).
- 25,000 cCREs sampled without replacement from genome-wide registry,
  200bp centered on midpoint, N-windows skipped.
- Combined and shuffled. GC ~44%.

## Purpose
Test the "mix" hypothesis: combining random genomic (preserves SK-N-SH
freebie) with cCRE (unlocks K562/HepG2) should beat both pure
strategies. Predicted mean_r > both 002 (0.150) and 004 (0.143).

## Result — **best so far**
mean_r ≈ 0.156. Beats 002 on 9/14 evals; beats 004 on 11/14 evals.
- K562_r: mostly +0.01 to +0.03 (small but consistently positive on
  most evals). One outlier: eval_10 = -0.046.
- HepG2_r: identical to K562_r (collapsed).
- SK-N-SH_r: 0.42–0.50 across evals (best at 0.50 on evals 06, 11).
- eval_06 and eval_11 record-best: mean 0.187.
- eval_07 record-best: 0.174.
- eval_08 still worst at 0.04 (no library cracks this).

## Interpretation
The MIX hypothesis is **confirmed**. Combining random genomic and
cCRE-centered windows preserves the SK-N-SH freebie *and* enables
K562/HepG2 signal. The two component populations are complementary
rather than redundant.

Most evals improved or held. The exceptions:
- eval_10: K562_r went negative (-0.05). This eval seems anti-cCRE
  in some way — maybe its targets aren't well-modeled by enhancer
  motif grammar.
- eval_08: still uniquely poor (0.04). Some kind of qualitatively
  different test set that my libraries don't address. Worth deeper
  investigation later.

## Theory update (T4 → T5)
- A good library is a **convex combination**: positives (regulatory
  elements) + diverse negatives (random genome) together. Each
  contributes a different signal that the other lacks.
- The model can use cCRE windows to learn motif grammar AND random
  windows to learn what "background" looks like, distinguishing them.
- Different evals reward different components; broad evals require
  broad coverage.

## What to try next
**Experiment 006 candidates** (ranked by expected information):
1. Test mix RATIO — is 50/50 optimal or is more cCRE better?
   006: 25/75 random/cCRE.
2. Stratified cCRE: equal proportions of PLS, pELS, dELS, CTCF-only
   plus random genomic. Tests whether type diversity matters.
3. Use rDHSs (~3.5M) instead of cCREs — finer regulatory diversity.
4. Investigate eval_08 specifically (need ideas first).

Going with 006 = 25/75 cCRE-heavy mix. Cleanest single-variable test
that builds on the 005 win.
