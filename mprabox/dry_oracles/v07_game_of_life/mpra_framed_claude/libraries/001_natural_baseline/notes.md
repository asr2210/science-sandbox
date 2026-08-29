# Experiment 001 — natural genomic baseline

## Design
50K random 200bp windows from hg38 primary chromosomes (chr1-22,X,Y),
length-weighted chromosome sampling, N-windows rejected. Seed=0.

## Result
- eval_01: 0.388 | best eval_13: 0.407 | worst eval_08: 0.257
- K562: 0.60 | HepG2: 0.42 | SK-N-SH: 0.14

## What I learned
1. **v07 is harder than v04.** Pure natural in v04 hit eval_01 ≈ 0.48;
   here it hits 0.39. Either the eval distribution differs, the model
   architecture differs, the measurement noise differs, or some
   combination. My v04 priors need recalibration before trusting.
2. **K562 ≠ HepG2 in v07.** In v04 they were identical. Now K562=0.60,
   HepG2=0.42, SK-N-SH=0.14. These are real, distinct cell types.
3. **SK-N-SH is the bottleneck.** Per-cell-type, SK-N-SH lags badly.
   This is the cell type that drags mean_r down. Boosting SK-N-SH is
   the highest leverage knob.
4. **eval sets cluster.** eval_02 = eval_05 = eval_14 (0.388 exactly).
   eval_04 = eval_09 (0.387). eval_03 = eval_12 (0.383). eval_06 =
   eval_11 (0.385). So ~7 distinct evals dressed as 14.
5. **eval_08 is hardest, eval_13 is easiest.** eval_07 is also fairly
   easy. eval_10 is slightly hard.

## Implications for next experiments
- The big question: can I lift SK-N-SH without sacrificing K562/HepG2?
- SK-N-SH is a neuronal cell line. Maybe neural enhancers / brain-active
  regulatory elements are under-represented in random genomic windows.
- Or maybe SK-N-SH is inherently noisier in the MPRA assay.
- Need to first confirm that the natural baseline holds up (it does
  here) before adding regulatory elements.
