# 015_sat_plus_motif_amplified

## Design
50K = 5K cCREs × 5 natural tiles (25K saturating half)
    + 5K cCREs × 5 motif-amplified tiles (25K)

Amplified tile = same natural window with 3 JASPAR vertebrate
motif instances (sampled from each motif's PFM) inserted at random
non-overlapping positions.

## Hypothesis (T10)
The model is saturated by 5K natural cCREs. The 25K freed budget
should be productive if filled with content that teaches something
the natural distribution doesn't — here, artificially elevated
motif densities in real genomic context.

## Result vs 005 / 012
                eval_01  K562    HepG2   SKNSH
005 cCRE dense: 0.3177   0.146   0.185   0.622
012 RC aug:     0.3195   0.144   0.191   0.624
015 motif-amp:  0.3167   0.144   0.180   0.626

DOWN by 0.001 vs 005. Slight HepG2 drop (0.005). SKNSH slight up.

## Interpretation
Motif-amplification ON realistic backbone is ~neutral. Better
than 006 (pure synthetic, 0.221) because the genomic backbone is
preserved, but adds nothing the model needs.

Pattern across all OOD-additive designs:
- 004 cCRE + shuffled:  0.3116 (hurts)
- 008 cCRE + random:    0.3091 (hurts)
- 015 cCRE + motif-amp: 0.3167 (~neutral)

The "OOD additive" axis is not productive when the OOD content is
distributionally close to the eval task (motif densities not present
in nature) or compositionally degenerate (random/shuffled).

## Theory T10 → T11
Saturating + additive-OOD pattern fails for every OOD type I've
tested. The freed 25K of budget is essentially un-usable for
within-genome-style content (whether natural or synthetic), at
least with these designs.

The remaining unexplored axes are:
1. **Conservation** (phastCons / phyloP) — evolutionary signal,
   strongest cross-species transfer prior.
2. **Cross-species enhancers** (mouse/zebrafish VISTA) — same
   transfer prior, different distribution.
3. **Cell-type-deep stratification** (per-cell-type DHS top-N for
   each cell type, 16.7K each).
4. **Very low region count, very dense** (1K cCREs × 50 tiles)
   to probe BELOW saturation in a tight, ultra-dense regime.
5. **VERY HIGH region count, single tile** (50K cCREs × 1 tile)
   to probe whether saturation = ~5K regions × 5 tiles is the same
   as ~25K regions × 1 tile, or whether per-region density matters
   at extreme breadth.

## Next
Experiment 016: PhastCons-element-filtered cCREs. Restrict cCRE
selection to those overlapping a phastCons conserved element (top
5% conservation), then 5K conserved cCREs × 10 tiles = 50K.

Generalization justification: phastCons-conserved cCREs are the
regulatory regions that selection has preserved across mammals.
They concentrate functional bases at higher density than typical
cCREs. A model trained on conservation-filtered content learns
"what evolution preserves" — universally applicable to any cell
type's regulatory prediction.
