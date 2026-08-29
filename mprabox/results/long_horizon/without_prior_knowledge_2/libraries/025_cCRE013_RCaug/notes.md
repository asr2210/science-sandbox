# 025 — 013 cCRE with reverse-complement augmentation

## Design
Same per-class counts as 013 (10K rare + 2.5K abundant). For each
class, draw 2.1*N distinct cCREs and emit the first N forward, the
next N as reverse-complement. Same total per-class count, half are
RC of different cCREs. Per-class diversity matches 013 in count
of distinct cCREs.

## Results (mean over 3 seeds)
- eval_01 = **0.7103** (vs 013 0.7477 = **-0.037**)
- mean across 14 evals = **0.7466** (vs 013 0.7900 = **-0.043**)
- eval_08 = 0.6403 (vs 013 0.7044 = **-0.064**)

## Per-eval delta vs 013
01:-0.037 02:-0.040 03:-0.043 04:-0.031 05:-0.038 06:-0.040 07:-0.059
08:-0.064 09:-0.037 10:-0.049 11:-0.037 12:-0.039 13:-0.053 14:-0.040

Uniformly negative, ~-0.040 across most evals. eval_07/08/13
hardest hit.

## Per-seed eval_01
seed 0 (spark01): 0.7004
seed 1 (local):   0.6899
seed 2 (spark03): 0.7405
SD ≈ 0.022 — wider than 013's typical 0.017.

## What this teaches
**T23 (new — RC augmentation hurts here):** Library-level RC
augmentation costs ~0.043 in mean. This rules out the "free lift"
hypothesis. Three plausible explanations:

1. **prepare.py training already RC-augments internally.** Adding
   library RC then duplicates effort but with cCRE-class labels
   that may be strand-asymmetric (e.g., cCRE class assignment uses
   stranded features like CpG-island promoter context).
2. **The oracle/surrogate model is strand-sensitive.** If oracle(S)
   ≠ oracle(RC(S)) for cCRE-like sequences, training on both
   creates contradictory regression targets.
3. **Effective per-cCRE coverage halves for the RC-flipped half.**
   Forward cCREs train the model on A; RC cCREs train the model
   on RC(A) — but the prediction target is the activity of A, not
   of RC(A). Strand-different effective signal.

Most likely (1) or (2) — model behavior or oracle is strand-aware.

**T17 / T20 unchanged.** This is a pipeline-interaction finding,
not about the regulatory-unit theory.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.

## Most informative next experiment (026)
We've ruled out:
- Mixing label-divergent sources (024)
- Library-level RC augmentation (025)

Promising direction: combine 013 (cCRE-only) with 022 (cCRE+random
flank chimeric) at sequence level. Both anchor on cCRE peaks (so
NOT label-divergent like 024), but the chimeric half should bring
the eval_08 boost (022's +0.049). This is the "best of both"
hypothesis.

**026 = 25K from 013 recipe + 25K from 022 chimeric design.** 50K
total, shuffled. ALL cCREs eligible.

Branches:
- 026 mean ≥ 0.7900 AND eval_08 ≥ 0.73 → bridges; new alt-best
- 026 ≈ 022 (mean ~0.787, eval_08 ~0.75) → mix matches 022 more
  than 013 — chimeric half dominates
- 026 < 013 mean by more than 0.005 → mixing two cCRE-anchored
  designs still hurts; abandon mix idea entirely
