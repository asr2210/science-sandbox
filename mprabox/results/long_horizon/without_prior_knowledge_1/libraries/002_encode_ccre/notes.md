# 002_encode_ccre — notes

## Design
50,000 sequences x 200 bp from ENCODE SCREEN cCREs (Registry V4, GRCh38).
Class-balanced: 6,250 sequences from each of 8 SCREEN classes (dELS,
pELS, PLS, CA, CA-CTCF, CA-H3K4me3, CA-TF, TF). For each cCRE, the
central 200-bp window (extending into flanking sequence if cCRE < 200 bp).
Sequences containing N rejected and re-drawn. Mean GC = 0.47, sd = 0.11
(vs. uniform random 0.50, sd ~0.035).

## Hypothesis
Real human regulatory DNA contains TF motif content and motif syntax
absent from random. Predicted: eval_01 mean_r ≥ 0.75 with bigger gains
on the low-baseline evals (07, 11, 12, 13).

## Result vs. random baseline (Δ = cCRE − random)

| eval | random  | cCRE    | Δ        |
|------|---------|---------|----------|
| 01   | 0.6954  | 0.7133  | +0.018   |
| 02   | 0.7848  | 0.8046  | +0.020   |
| 03   | 0.7612  | 0.7870  | +0.026   |
| 04   | 0.7494  | 0.7733  | +0.024   |
| 05   | 0.6951  | 0.7133  | +0.018   |
| 06   | 0.7853  | 0.8048  | +0.020   |
| 07   | 0.6684  | 0.7452  | **+0.077** |
| 08   | 0.7841  | 0.6380  | **−0.146** |
| 09   | 0.8115  | 0.8385  | +0.027   |
| 10   | 0.7564  | 0.7635  | +0.007   |
| 11   | 0.6833  | 0.7010  | +0.018   |
| 12   | 0.6553  | 0.6757  | +0.020   |
| 13   | 0.6584  | 0.7422  | **+0.084** |
| 14   | 0.7851  | 0.8046  | +0.020   |

Mean across evals: 0.738 → 0.748 (+0.010 average — modest).

## Interpretation
**Biology helps, but unevenly. Most importantly: eval_08 collapses.**

Three distinct response classes among the 14 evals:
- **Modest +0.02 across the board** (01, 02, 03, 04, 05, 06, 09, 11, 12, 14):
  natural regulatory DNA gives a small but consistent lift.
- **Big wins** (07: +0.077, 13: +0.084): these evals reward biological
  grammar substantially. Both were among the low-baseline group on random,
  so this is exactly where I predicted headroom would be available.
- **Big loss** (08: −0.146): eval_08 actively rewards a random-like
  training distribution. It must contain sequences whose activity is
  predictable from generic composition but not from natural motif
  content — possibly synthetic / scrambled / random sequences themselves.

Cluster correction: I previously grouped {02, 06, 08, 14} at ~0.785
based on random-baseline scores. With cCRE training, 08 falls to 0.64
while 02/06/14 stay at 0.80. So **eval_08 is qualitatively different
from 02/06/14** — they only coincided at the random floor.

eval_01 ≈ eval_05 still holds (both 0.7133), confirming the pairing.

Per-cell-type ordering: still SKNSH > K562 ≈ HepG2 in essentially every
eval. Library-independent pattern, almost certainly assay-level.

Seed variability is noticeably higher than random library (cCRE eval_01
seeds: 0.702 / 0.740 / 0.697 — sd ~0.02 vs random sd ~0.003). Likely
because biology has higher between-sample variance per 50K draw.

## What this changes
1. Most of the eval signal IS captured by composition alone (random gets
   to ~0.74 mean already). Biology adds only ~0.01 on average.
2. But there is real, large headroom on a subset of evals (07, 13)
   that responds to motif content.
3. There is at least one eval (08) that actively penalizes biology.
   A library that only tests cCREs would lose accuracy here.
4. The ideal library probably needs to be **a mixture** — biology for
   the motif-dependent evals, composition diversity for eval_08-like
   sets, and broad coverage everywhere.

## Next experiment
Disambiguate composition vs motif content. The most informative single
experiment: dinucleotide-shuffled cCREs. Take the same sequences as
this library but shuffle each one preserving dinucleotide frequencies.
This destroys motif syntax while preserving local composition. If
shuffled cCREs match this experiment's results → composition explains
everything. If shuffled cCREs look like uniform random → motif content
is what matters. Result will be in between — the gap tells us how much
of the cCRE gain is motif-driven.
