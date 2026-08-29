# Experiment 003 — Zero-diversity diagnostic

## Hypothesis
50K identical copies of a packed motif sequence. Two possible outcomes:
- Per-seq metric → score = that one sequence's score
- Library-level metric → score crashes near zero

## Method
One synthetic 200bp sequence built by repeating motif blocks
(TATA, SP1, NFY, E-box, CRE, AP-1, GATA, ETS, OCT, NeuroD) joined
by short "AC" spacers. 50K identical copies.

## Results
All eval sets returned NaN with the warning:
  "ConstantInputWarning: An input array is constant;
   the correlation coefficient is not defined."

## Interpretation — BIG INSIGHT
The metric IS Pearson correlation. One axis of the correlation is
a function evaluated per library sequence. When all sequences are
identical, that vector is constant → r undefined.

So `mean_r` is NOT "mean predicted activity" — it is correlation
between two vectors, each of length ~N_library, evaluated on my
sequences.

Most likely candidates:
- corr(model_A_pred(seq), model_B_pred(seq))  — cross-model agreement
- corr(model_pred(seq), ground_truth_label(seq)) — where label is
  some function the oracle defines (e.g., another model, a derived
  feature, or a fixed answer per sequence)

In all cases, to MAXIMIZE r, library sequences must:
1. Have DIVERSITY in the underlying signal (no constant or near-constant
   predictions) — explains why random > cocktail (more diverse
   predictions)
2. Be IN-DISTRIBUTION for whatever models the oracle uses. Real
   human DNA likely sits in-distribution; uniform random and motif
   cocktails are out-of-distribution.

## Theory update — T2
mean_r = correlation between two functions of library across its
50K sequences. To raise it, generate sequences that look like
natural human DNA — the models can then produce well-calibrated,
correlated outputs.

## Next
Exp 4: order-2 Markov-chain sequences with human-genome-like
dinucleotide frequencies (low CpG, AT-rich). Cheap and tests T2
without downloads.

If T2 holds, expect a meaningful uptick over random uniform.
