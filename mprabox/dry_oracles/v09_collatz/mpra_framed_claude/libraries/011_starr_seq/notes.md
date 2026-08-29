# 011_starr_seq

## Design
50,000 = 10,000 STARR-seq active peaks (top 5K K562 + top 5K HepG2
by peak score) × 5 random-offset 200bp tiles.

Source: ENCODE Gerstein-lab WG-STARRPeaker
- K562: ENCFF045TVA (36,108 peaks)
- HepG2: ENCFF047LDJ (52,650 peaks)

No SKNSH STARR-seq is available — K562/HepG2 only.

## Hypothesis (T8)
STARR-seq directly measures enhancer activity in a reporter context;
it is the closest functional analogue to MPRA among publicly
available datasets. If the plateau (0.318) is set by "sequences
need to be MPRA-like", these should produce the biggest single-source
lift. If they don't lift, the plateau is more likely architecture/
budget-bound than design-bound.

## Result vs 005 (cCRE dense)
                eval_01  K562    HepG2   SKNSH   eval_07  eval_08
005 cCRE dense: 0.3177   0.146   0.185   0.622   0.338    0.076
011 STARR:      0.2874   0.141   0.097   0.625   0.293    0.079

eval_01 DROPS by 0.030. HepG2 prediction nearly halves (0.185 → 0.097).
K562 unchanged. SKNSH unchanged. eval_07 (most grammar-sensitive)
also drops.

## Interpretation
STARR-seq peaks should be the BEST training source if the goal is
"MPRA-like sequences". They aren't. The HepG2 collapse is the
telling part:
- HepG2 STARR has 53K peaks; we took the top 5K by STARRPeaker
  score. Top STARR peaks are dominated by very strong, narrow-
  acting regulatory elements.
- These look like the housekeeping/strong-promoter contamination
  pattern from 009 (top DHS) — once again, high-signal filtering
  reduces VARIANCE and the model has nothing left to learn about
  what differentiates HepG2 activity.

Also, STARR is an episomal reporter; its active peaks reflect
sequences whose activity is plasmid-context, not chromatin-context.
This may mismatch the eval-MPRA's measurement modality.

## Theory T8 → T9
**Functional MPRA-likeness alone is insufficient.** Two reinforcing
lessons:
1. The plateau is robust to source-modality choice. STARR-seq,
   DNase, cCRE — all land near 0.29-0.32 (worse if signal-top-
   filtered, parity if diverse).
2. Top-signal filtering CONSISTENTLY hurts (009, 011 both lose
   HepG2). The lesson is general: "high-confidence regulatory
   peaks" make worse training data than DIVERSE regulatory peaks,
   because the model needs variance to learn.

Updated theory: The plateau is set by a combination of
(a) per-cell-type addressable variance ceiling — fixed by the model
    + 50K budget,
(b) the model's sample-efficiency on the natural-genomic
    distribution,
and is NOT moved by within-distribution source-refinement.

To break it, need either:
- A categorically different SCALE (huge density, RC augmentation,
  paired controls — multiply effective training pairs).
- A categorically different DISTRIBUTION (synthetic-grammar
  perturbation, conservation-filtered evolutionary signal,
  cross-species genomic regions).

## Next
Experiment 012: REVERSE-COMPLEMENT AUGMENTED dense cCREs.
Take the 005 design (10K cCREs × 5 tiles = 50K) but generate 25K
cCRE-tile + their 25K reverse complements. The model gets a strong
strand-invariance prior baked into training data without losing
sequence variety. This is the cheapest "categorical scale" lever
and tests whether the model is bottlenecked by strand-aware
sample efficiency.
