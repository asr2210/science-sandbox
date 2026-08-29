# Experiment 011 — TF-diversity-curated natural windows

## Design
Stream ReMap (68M peaks), bin by 200bp tile, score each tile by
|unique TFs|. Pick top 50K tiles, sample window centered at tile
midpoint with small jitter.

Top tile: 768 unique TFs. #50K cutoff: 146 unique TFs. So all 50K
windows have very dense TF binding — far more than typical cCRE.

## Result
- eval_01: 0.3831 (Δ **-0.0045 vs nat**, -0.013 vs 4-way mix)
- K562: 0.5926, HepG2: 0.4173, SK-N-SH: 0.1394
- eval_13 (peak eval): 0.3928 (vs 0.4090 in mix, -0.016)

**This is the WORST natural-source library I've tested.**

## Interpretation
Counterintuitive but strong signal: TF binding density does NOT
predict training value. Top-density tiles are likely:
- Heavily-studied promoter regions (housekeeping genes)
- Repetitive elements where many TFs cross-bind
- A narrow slice of genomic context (low diversity of compositions)

Loss of distributional diversity hurts more than the gain from
"regulatory grammar."

## Theory update — T7
**The right library isn't "most regulatory" — it's "best matched
to eval distribution."** Eval seems to expect broad natural coverage,
not deep regulatory coverage. Concentrating on the top of the
regulatory density curve narrows the model's effective training
distribution.

This contradicts the intuition that "more TF binding = more learnable
regulatory grammar" but is fully consistent with v07's narrow
dynamic range: the model is robust enough that *broad coverage*
matters more than *intense coverage*.

## Implication for next experiments
- Skip variant-rich, motif-density, conservation-curated libraries
  (all likely concentrated in similar non-representative regions)
- Test things that BROADEN natural coverage:
  - RC augmentation (each natural + its RC)
  - GC-stratified (uniform across GC bins)
  - Length-uniform tile sampling (sample EVERY non-overlapping
    200bp tile with equal probability instead of length-weighted)
