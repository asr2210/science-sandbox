# Experiment 006 — 25/75 mix (cCRE-heavy)

## Design
- 12,500 random genomic + 37,500 cCRE-centered windows. Shuffled.
- GC 46%. Single ratio variation from 005.

## Purpose
Test whether more cCRE content improves on 005 (50/50). Hypothesis was
"a bit more regulatory might continue to help".

## Result — **lost ground**
mean_r ≈ 0.134 (vs 005's 0.156).
- **K562_r turned negative** on most evals: −0.02 to −0.07.
- HepG2_r still tied to K562.
- SK-N-SH_r ~0.44 (similar to 005).
- eval_06 crashed: 0.187 → 0.117. Worst loss.
- eval_11 same crash (tied to eval_06).
- eval_07 also dropped from 0.174 to 0.160.
- eval_13 went up slightly (0.157 → 0.159).

## Interpretation
**More cCRE is not better.** The K562 prediction quality
actively degrades — the model overcommits to "active" predictions when
trained predominantly on regulatory elements, hurting it on evals
that test a wider activity range.

This is **theory-refining**: regulatory content is not a monotonic good.
There is an optimum around 50/50, and pushing past it actively hurts.

## Theory update (T5 → T6)
- **Optimum is around 50/50 random + cCRE.** Pushing toward more cCRE
  causes the model to over-predict activity in K562, manifesting as
  negative correlations.
- The model needs **enough negatives to learn the activity scale**, not
  just enough positives to learn the motifs.
- "Diversity" must include diversity in the *target* axis (activity),
  not just in input motif composition.

## What to try next
**Experiment 007**: 75/25 random-heavy (37.5K random + 12.5K cCRE).
Maps the other side of the ratio curve. If 007 is also worse than 005,
then 50/50 is a sharp local optimum.

If 007 happens to be better than 005, the optimum is even further
toward random — surprising but possible (more diverse negatives,
fewer noisy positives).

After 007, I'll know the ratio curve well enough to lock in a working
~50/50 baseline and move on to a qualitatively different question:
- WHICH cCREs matter (stratified)?
- WHAT other types of positives (rDHS, JASPAR motifs)?
- WHY eval_08 / eval_10 stay stubbornly hard?
