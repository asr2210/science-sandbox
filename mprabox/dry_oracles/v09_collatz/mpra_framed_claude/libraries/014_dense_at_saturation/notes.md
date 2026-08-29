# 014_dense_at_saturation

## Design
5,000 cCREs × 10 random-offset 200bp tiles = 50,000. Same region
count as 012 (saturating per 012/013 triangulation), pure
intra-region density at saturation, no RC.

## Hypothesis (T10)
If region count of 5K saturates the model on the natural cCRE
distribution, then doubling per-region tiles from 5 to 10 should
not lift eval_01 above 005's 0.3177 or 012's 0.3195.

## Result vs 005 / 012
                eval_01  K562    HepG2   SKNSH   regions x tiles
005 cCRE dense: 0.3177   0.146   0.185   0.622   10K x 5
012 RC aug:     0.3195   0.144   0.191   0.624   5K  x 5 (+RC)
014 dense @sat: 0.3181   0.144   0.188   0.623   5K  x 10

eval_01: 0.3181. **Parity with 005 and 012**.

## Interpretation — saturation confirmed
Three independent allocations of the 50K budget, all at or above
the saturation region count, give the same plateau:
- 10K regions × 5 tiles (005)
- 5K regions × 5 tiles + RC (012)
- 5K regions × 10 tiles (014)

This is strong confirmation that:
1. 5K diverse cCREs saturates the model's learning of the natural-
   genomic regulatory distribution.
2. Above this saturation, no within-distribution allocation
   (more regions, more tiles, more strand copies) moves the
   plateau.
3. The remaining 25K of budget capacity is effectively WASTED
   when filled with more of the saturated distribution.

## Theory T10 (confirmed)
The 50K budget is over-allocated to natural-genomic regulatory
content. Saturation = ~5,000 diverse cCREs × 5 tiles = 25K
sequences. Beyond that, additional capacity must come from a
distinct distribution or be discarded.

## Next
Experiment 015: hybrid library testing "saturation + OOD additive".
5K cCREs × 5 natural tiles (25K, saturated) + 5K cCREs × 5
motif-amplified tiles (25K). Each amplified tile = same natural
window with 3 randomly-placed strong JASPAR motifs inserted.

Generalization justification: motif-amplified cCREs let the model
see both natural compositional density (regulated by selection)
AND artificially elevated motif density. The latter pushes the
model out of its saturated comfort zone in the compositional
dimension while preserving realistic genomic backbone, addressing
the failure mode of 006 (pure synthetic scaffolds were too OOD).

Prediction: if the model has any unsaturated capacity for learning
compositional rules, this hybrid lifts eval_01. If 006-style OOD
"breaks" the model even when paired with saturating cCRE half,
this will be flat or down.
