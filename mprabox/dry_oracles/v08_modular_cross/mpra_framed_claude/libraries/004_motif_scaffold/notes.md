# Experiment 004 — Synthetic motif scaffold

## What I tested
50,000 sequences = 200 bp random uniform backbone with 0–10 canonical
TF motifs inserted (uniform pos, random strand). Motif pool: AP-1,
ETS, NRF1, USF/E-box, KLF/SP1, CTCF, MEF2, CREB, NFY, YY1, HNF1,
HNF4, FOXA, CEBP, GATA1, TAL1, RUNX, REST, ZBTB, TATA, STAT, IRF,
NF-κB, AR. Mean inserts/seq = 5.0.

## Hypothesis
Strong motif signal on random backbone should give the model a wide,
predictable activity range and beat baselines substantially.

## Result
- eval_01 = 0.0052 (baseline ~0)
- K562 reached r=0.017–0.018 on several evals — the largest cell-type-
  specific signal so far in any experiment.
- HepG2/SK-N-SH stayed near zero.

## What this tells me
Motifs help, but weakly. Possible reasons:
1. Five motifs in 200 bp may be too sparse — most of the sequence is
   still random.
2. The motif pool may overweight weak motifs and underweight known
   strong activators.
3. K562 is most responsive because the pool contains GATA, TAL1,
   RUNX, ETS — hematopoietic-biased — and these all activate K562.
4. The MPRA simulator inside prepare.py may have a noise floor that
   our current activity range doesn't escape.

## Updates to theory
- Motif-based design is on the right track.
- Need higher motif density and a curated, stronger pool.
- The fact that K562 specifically responds to a hematopoietic-biased
  motif set strongly hints the underlying MPRA models in prepare.py
  ARE motif-aware.

## Next
Increase motif density (10–20 inserts), curate stronger pool, and
include explicit high-activity sequences to widen dynamic range.
