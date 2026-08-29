# 012_rc_augmented

## Design
5,000 cCREs × 5 random-offset 200bp tiles = 25,000 forward tiles.
+ reverse-complement of each = 50,000 total.

Region budget halved vs 005 (5K instead of 10K cCREs), but each
region's content presented as both strands.

## Hypothesis (T9)
Source-modality refinement is exhausted. Test a categorically-
different scale lever: explicit RC augmentation. TF binding is
strand-invariant by physics; bake that prior into the data and the
model gets stronger sample efficiency per region.

## Result vs 005 (cCRE dense)
                eval_01  K562    HepG2   SKNSH   eval_07  eval_13
005 cCRE dense: 0.3177   0.146   0.185   0.622   0.338    0.327
012 RC aug:     0.3195   0.144   0.191   0.624   0.338    0.328

eval_01 +0.0018 (new high). HepG2 +0.006, SKNSH +0.002, K562 -0.002.
eval_07 unchanged, eval_13 +0.001.

## Interpretation
Marginal lift (~noise), but the direction is consistent across all
3 cell types except K562. Most importantly: the lift is ROUGHLY
ZERO. This says:
- The model is mostly strand-robust already (architectural or
  training-time symmetry, likely RC convolutions).
- Halving the region budget did NOT hurt performance. This is the
  important sub-result: **the model is not region-budget-bound**.
  We can free up 50% of the sequence budget without losing eval_01.

The freed-budget finding is the lever I should pull harder. If 5K
unique regions × (5 tiles + 5 RC tiles) ≈ 10K unique regions ×
5 tiles, then the model's effective capacity is saturated
somewhere BELOW 10K regions of cCRE diversity. Adding more regions
buys nothing; adding more per-region variance also buys nothing.
The bottleneck is elsewhere.

## Theory T9 → T10
Region count, tile count per region, signal source, differential
stratification, and reporter-modality all hit the same plateau
because they vary axes the model is already saturated on. The
plateau is set by a SCALABLE axis I haven't perturbed yet.

Two remaining categorically-different levers:
1. **OUT-OF-DISTRIBUTION structure** — synthetic motif perturbations
   that the natural genome doesn't sample (motif densities, motif
   combinatorics, motif spacing) that force the model to learn
   compositional rules rather than memorize regional patterns.
2. **MULTI-TASK / multi-context** structure — sequences that
   represent contexts the model can't reach from the genome alone
   (extreme GC, conservation extremes, multi-cell-type-specific
   junctions).

## Next
Experiment 013: SATURATION MUTAGENESIS-style perturbed cCREs.
Take 2,500 strong cCREs, generate 20 sequences per cCRE: 1 wild-
type tile + 19 single-position substitutions (~1 mutation per 10bp
spread across the tile). Total 50,000 sequences. The model learns
HOW MUCH each base position contributes to activity — directly
analogous to what an MPRA's downstream interpretation does. This
is a categorical structural shift: paired-comparison training
pairs rather than independent draws.

Generalization justification: per-position effect prediction is the
fundamental atomic unit of regulatory grammar. A model that learns
this learns rules that apply universally, not patterns specific
to K562/HepG2/SKNSH.
