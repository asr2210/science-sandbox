# Experiment 007 — Dense motif scaffolds (15-25 motifs / seq)

## What I tested
50,000 sequences, random uniform 200 bp backbone, 15–25 inserts each
from a curated 33-motif pool spanning universal (AP-1, ETS, NRF1, USF,
SP1, CREB, CTCF, NFY, MEF2), hematopoietic (GATA, TAL1, RUNX, MYB,
NFE2, KLF, STAT5), liver (HNF1, HNF4, FOXA, CEBP, PPARA, HNF6), and
neural (NEUROD, ASCL1, BRN2, FOXG1, PAX6, LHX, TBR1, PHOX2, REST).
Both strands.

## Hypothesis
Motif density should scale signal. Going from 0–10 (exp 004) to 15–25
should boost activity range and predictability.

## Result — first signs of SK-N-SH and broader cell-type response
- eval_07: mean = 0.0061 (highest mean across all experiments so far),
  SKNSH = 0.0126 (highest SK-N-SH signal seen anywhere)
- K562: 0.005–0.010 broadly
- HepG2: 0.004–0.006 broadly
- SKNSH: 0.005 on eval_04/09, 0.013 on eval_07, but negative on
  several others — still inconsistent
- Mean across evals ≈ 0.003

## What this tells me
1. Density helps. Going from sparse (mean 5) to dense (mean 20)
   motif inserts gave a real, multi-cell-type signal lift.
2. The signal is now BROADER (K562+HepG2+SKNSH all sometimes
   positive) but still concentrated on specific evals.
3. eval_07 is unusually responsive to dense motif content. This eval
   may be testing on heavily motif-loaded sequences.

## Updates to theory
- **Motif density is a clear lever.** More motifs → wider activity
  range → more learnable signal.
- A *mixed* pool of motifs (universal + cell-type-biased) is better
  than splitting into separate pools by cell type — because dense
  scaffolds saturate the regulatory grammar.
- The next ~3-5 cell types to push are: SK-N-SH consistency, HepG2
  broad coverage, and discovering whether further density pushes
  signal even higher.

## Next
Combine dense motif scaffolds (good across cells) with TSS promoters
(strong HepG2 boost) in a 50/50 split.
