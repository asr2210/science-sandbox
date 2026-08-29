# 013 — Stratified GC mix, 10 bins × 5k

## What I tested
50k chr22 200bp windows stratified into 10 equal-quantile GC bins
(GC ranges: 0.00-0.345, 0.345-0.380, 0.380-0.410, 0.410-0.440,
0.440-0.470, 0.470-0.500, 0.500-0.525, 0.525-0.555, 0.555-0.600,
0.600-0.915), 5000 per bin. Random orientation. Seed=42.

## Result — marginal eval_01 win, marginal mean loss
- eval_01 = **0.1375**  (012: 0.1367, +0.0008 — new best)
- mean of evals = 0.1298 (012: 0.1308, -0.001)
- K562: 0.043 (012: 0.038, +0.005) ← biggest gain
- HepG2: 0.170 (012: 0.174, -0.004)
- SK-N-SH: 0.200 (012: 0.198)

## What this means
Diminishing returns on bin granularity. Going from 5 to 10 bins gives
~no additional gain — eval_01 nudged +0.001, mean dropped -0.001.
This suggests 5-bin stratification already captured most of the
compositional-breadth benefit.

The K562 jump (+0.005) is notable but small in absolute terms.

## Theory update
"Compositional breadth helps" is real but finite. The right number
of bins is small (5 is sufficient). The plateau near 0.137-0.138 is
the new ceiling for GC-only stratification on chr22.

To break further I need a NEW axis of diversity:
- Other compositions (CpG content, AT-skew, complexity/entropy)
- Other chromosomes (chr13 AT-rich, chr19 GC-rich, X for divergence)
- Joint stratification on 2 axes
- Synthetic interpolation between natural sequences

## What to try next
014: CpG-content stratification (independent of GC). CpG islands are
the most biologically distinctive dinucleotide pattern and likely an
independent axis from GC content. 5 CpG-density bins × 10k each.
