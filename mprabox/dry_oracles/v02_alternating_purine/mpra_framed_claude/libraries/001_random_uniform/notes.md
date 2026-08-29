# Experiment 001 — pure uniform-random sequences

## Design
- 50,000 sequences of length 200bp
- Each base sampled iid from {A,C,G,T} with p=0.25
- Seed: 0
- No regulatory grammar, no genomic structure, no motifs

## Purpose
Establish the floor of model performance with zero regulatory information
in the training library. A control against all later designs.

## Result
| eval | mean_r | K562_r | HepG2_r | SKNSH_r |
|------|--------|--------|---------|---------|
| 01 | 0.116 | -0.004 | -0.004 |  0.357 |
| 02 | 0.116 | -0.006 | -0.006 |  0.358 |
| 03 | 0.127 | -0.006 | -0.006 |  0.392 |
| 04 | 0.120 | -0.004 | -0.004 |  0.369 |
| 05 | 0.116 | -0.006 | -0.006 |  0.358 |
| 06 | 0.124 | -0.010 | -0.010 |  0.393 |
| 07 | 0.136 |  0.010 |  0.010 |  0.389 |
| 08 | 0.052 | -0.000 | -0.000 |  0.156 |
| 09 | 0.120 | -0.004 | -0.004 |  0.369 |
| 10 | 0.127 |  0.004 |  0.004 |  0.372 |
| 11 | 0.124 | -0.010 | -0.010 |  0.393 |
| 12 | 0.127 | -0.006 | -0.006 |  0.392 |
| 13 | 0.123 |  0.006 |  0.006 |  0.358 |
| 14 | 0.116 | -0.004 | -0.004 |  0.357 |

Time: 49 s.

## Observations
1. **K562 and HepG2 are essentially uncorrelated** with eval truth.
   The model learned ~nothing about these cell types from random
   sequences. Expected.
2. **K562 and HepG2 predictions are identical numerically** (to 4 sig
   figs) for every eval — likely the model collapsed both heads to the
   same near-constant output (mean-predictor) since random sequences
   carry no signal that would let it differentiate.
3. **SK-N-SH is unexpectedly correlated** (~0.36 across evals). With a
   completely uninformative training set, this is suspicious. A few
   possibilities:
   - SK-N-SH eval activity is dominated by a simple feature (e.g.
     GC content, total nucleotide composition) that even a near-trivial
     model can capture from random training data.
   - The model collapses to predicting a constant in SK-N-SH that happens
     to correlate via something like length or composition.
   - Either way: the "free" 0.36 is the floor for SK-N-SH; only the
     mean_r above ~0.12 reflects genuine learning from a library.
4. **eval_08 is an outlier**: mean=0.05, SK-N-SH=0.16. Either much harder
   or measures something orthogonal to what random sequences can predict.
   Worth watching across experiments.
5. **Several evals are numerically identical** (01=14, 02=05, 03=12,
   04=09, 06=11). Suggests these eval sets share underlying truth or
   sequences and differ only in re-sampling. Useful: I effectively have
   ~8–10 distinct evals, not 14.

## Updates to theory
- The 0.12 baseline is mostly a SK-N-SH artifact. To measure real
  *learning*, I should track K562_r and HepG2_r (currently ~0) and how
  much SKNSH_r rises above 0.36.
- Working baseline / null: mean_r ≈ 0.12, K562_r ≈ 0, HepG2_r ≈ 0,
  SKNSH_r ≈ 0.36. Real-information-content libraries should push K562
  and HepG2 above 0 and SKNSH above 0.36.

## What to try next
Experiment 002: random 200bp windows sampled from real human genome
(probably chr22 for speed). Tests whether *any* real DNA — without
regulatory enrichment — already adds signal beyond uniform random. This
isolates the effect of "natural sequence statistics" from regulatory
grammar.
