# Experiment 024 — 35k motifs (10 universal TFs) + 15k pELS

## What I tested
Restricted motifs to 10 "universal" TFs (SP1, NRF1, ETS, USF, AP1,
CREB, NFY, YY1, TATA, INR) — removed all cell-type-specific TFs.
Tests if universal-only TFs preserve mean (generalization-friendly)
or kill it.

## Result — broadly negative
- eval_04/09: 0.0041 (decent)
- eval_07: mean=0.0052, HepG2=0.0091 (decent)
- Most broad evals NEGATIVE (01,02,05,06,11,13,14)
- eval_08: -0.0017 (lost)
- eval_10: -0.0020 (lost)
- Mean across 14 ≈ -0.0005

## What this tells me
**Cell-type-specific TFs are doing meaningful work in 012.** The
GATA1/TAL1/HNF1/HNF4/NEUROD/ASCL1/etc. motifs aren't noise — they
contribute features the model uses to predict K562, HepG2, SK-N-SH
activity respectively.

Restricting to universal-only motifs lost most of the per-cell-type
signal. The model has nothing cell-type-specific to learn.

## Updates to theory
**v3.15 → v3.16:** The optimal motif vocabulary spans:
- ~10 universal TFs (broad coverage)
- ~25 cell-type-specific TFs (per-eval specialization)
Total ~35, which is what 012/007 had. Both halves are needed.

This is actually GOOD NEWS for generalization: a model trained on
cell-type-specific TFs learns features that, while specific to those
TFs, generalize to ANY cell type using those TFs. Removing them
removes the model's ability to learn the features at all.

## Next
Test 012 stability: re-run 012 recipe with a different RNG seed
to see if mean=0.0029 is the recipe's stable value or a lucky draw.
If reproduces ±0.0005, the ceiling is firm. If varies more, there's
randomness room.
