# 019_hepg2_optimized

## Design
5,000 HepG2-SPECIFIC DHS peaks (HepG2 DHS not overlapping K562 or
SKNSH within 200bp window) × 10 random-offset tiles = 50K.

Selected top 5K by HepG2 signal (max_density). Tests whether
maximally pushing HepG2-specific exposure lifts the HepG2 head
past ~0.19.

## Result vs 014 / 010
                eval_01  K562    HepG2   SKNSH
014 5K x 10:    0.3181   0.144   0.188   0.623
010 diff DHS:   0.3180   0.139   0.188   0.628
019 HepG2-opt:  0.2808   0.143   0.095   0.605

eval_01 DROPS by 0.037. HepG2 prediction nearly halves (0.188 →
0.095). K562 unchanged (library-insensitive). SKNSH drops slightly.

## Interpretation — the worst result of any single-source design
HepG2-specific top-signal-filtered library DESTROYS HepG2
prediction. Same pattern as 009 (top DHS) and 011 (top STARR).

Combined with 010 (HepG2-specific got 0.188 when paired with K562/
SKNSH/shared classes), this proves:
- **HepG2-only training is worse than HepG2 + diversity training**.
- The HepG2 head needs CROSS-CELL-TYPE variance in the training
  distribution to discriminate HepG2 activity from K562/SKNSH
  activity.
- HepG2-specific peaks (with K562/SKNSH excluded) become a
  low-variance feature space — the model can't tell which features
  drive HepG2 vs the absent comparison cell types.

## Theory T12 → T13 (architecture-bound HepG2 ceiling)
HepG2 head's ~0.19 ceiling is ALSO architecture-bound for this
model + budget on natural-genomic content. It cannot be pushed
higher by more HepG2 content; it requires CROSS-CELL-TYPE diversity
to discriminate.

The plateau at 0.318 is genuinely the model × budget × natural
distribution ceiling. All three per-cell-type heads are saturated:
- K562 ≈ 0.146 (library-insensitive entirely)
- HepG2 ≈ 0.19 (only in cross-cell-type-diverse libraries)
- SKNSH ≈ 0.625 (mostly library-insensitive, slight variation)

## What is left to test
The remaining hypothesis space is small. Some unexplored axes:
1. **Cross-species enhancers** (mouse/zebrafish + VISTA validated):
   would the model benefit from non-human regulatory grammar?
2. **Eval-set-specific optimization**: eval_08 is anti-cCRE,
   eval_07/13 are pro-cCRE. Are there cocktail designs that lift
   the WEAK evals without sacrificing the strong ones?
3. **Larger-window sampling** (tiles from ±400bp instead of ±100bp
   from cCRE midpoint): more context exposure per region.
4. **All-cell-type DHS coverage**: rDHS / cCRE BROAD already
   approximates this and showed parity.

## Next
Experiment 020: WIDER tile-position sampling. 5K cCREs × 10 tiles,
each tile drawn from uniform random offset in ±400bp (instead of
±100bp). Tests whether broader CONTEXT exposure per region adds
something that within-cCRE-core tiling doesn't.

Generalization justification: enhancer activity depends on
flanking context (insulator distances, neighboring TFs). Wider
sampling exposes the model to the regulatory context surrounding
the core element, teaching context-aware grammar that transfers
to any cell type's regulatory landscape.

Prediction: parity to slight lift. If lift, context-aware sampling
is a previously-unexplored axis.
