# 013_sat_mut

## Design
2,500 cCREs × 20 sequences = 50K. Per cCRE: 1 WT + 19 mutants,
each mutant has 5 random single-base substitutions.

## Hypothesis (T9 → T10 candidate)
Paired wt/mutant training pairs teach per-position effects ——
the atomic unit of regulatory grammar. Could be a categorically
different source of learning than independent regional draws.

## Result vs 005 / 012
                eval_01  K562    HepG2   SKNSH
005 cCRE dense: 0.3177   0.146   0.185   0.622
012 RC aug:     0.3195   0.144   0.191   0.624
013 sat-mut:    0.3036   0.135   0.154   0.622

DOWN by 0.014. HepG2 down by 0.031. K562 and SKNSH ~ unchanged.

## Interpretation
Paired comparison does NOT teach better than independent draws. Why:
- 5-position mutants are near-WT. Their measured activity is
  near-identical to WT. The model gets thousands of "tiny delta"
  pairs that compress label-space variance.
- Only 2,500 unique regions — half of 012, a quarter of 005. The
  K562/HepG2 head loses representation diversity.

## Combined with 012 — saturation point identified
- 012: 5K regions × (5 fwd + 5 RC) → eval_01 0.3195
- 005: 10K regions × 5 tiles      → eval_01 0.3177
- 013: 2.5K regions × 20 mutants  → eval_01 0.3036

**The model saturates on natural-genomic cCRE diversity at
~5,000 unique regions.** Below saturation, region count is the
bottleneck and intra-region density cannot compensate. At or above
saturation, more regions don't help and per-region density doesn't
help either — within the natural-genomic distribution.

## Theory T10
The 50K budget is over-allocated for natural-genomic regulatory
content. The model needs roughly 5K diverse cCREs × 5 tiles = 25K
sequences to saturate its learning of the natural distribution.
Beyond saturation, additional capacity should be spent on a
**distinct distribution** that teaches something natural cCREs
don't.

## Next
Experiment 014: 5,000 cCREs × 10 random-offset tiles = 50,000.
Pure intra-region density at the saturating region count. If this
matches 012/005 (~0.318), confirms "more tiles ≠ better at
saturation". If it lifts past 0.32, intra-region density at
saturation IS the lever.

Note: I expect ~0.318 (parity). The follow-on 015 will spend the
"freed budget" of 25K sequences on synthetic motif-planted
sequences (the OOD distribution I haven't successfully tested
yet, since 006 used PURE synthetic which didn't work — try a
HYBRID 5K cCREs × 5 tiles + 25K synthetic instead).
