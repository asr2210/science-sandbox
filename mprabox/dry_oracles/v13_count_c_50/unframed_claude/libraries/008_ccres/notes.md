# 008_ccres

## What
50K sequences, each = 200bp window centered on the midpoint of a randomly-chosen ENCODE V3 cCRE (chr1 + chr22). 118K cCREs available.

## Why
Test whether regulatory-enriched natural sequences beat plain random hg38 windows.

## Results
eval_01: **0.4627** (vs 0.5408 random hg38 → -14%)
- K562_r: 0.597 (vs 0.586) +tiny
- HepG2_r: 0.397 (vs 0.520) -down
- SKNSH_r: 0.394 (vs 0.517) -down

BUT eval_04/09: 0.580 (vs 0.469), eval_08: 0.415 (vs -0.039) — strongly UP.

GC stats: mean 0.499, std 0.096 (similar variance to random hg38).

## Interpretation
cCREs are **less diverse** in the dimensions eval_01 cares about. Random hg38 includes AT-rich repeats, intergenic deserts, etc. — broader compositional variance → higher r on eval_01.

Different eval sets reward different sequence-type distributions. cCREs are GOOD for evals that prefer regulatory features (eval_04/09, eval_08), BAD for evals that prefer broad compositional spread (eval_01/02/03/05/06/07/11/12/13/14).

## Takeaway
Plain random hg38 is the winner so far for eval_01. To beat it, need **more compositional variance**, not less. Try mixing natural + extreme-GC synthetic, or natural from multiple chromosomes with stratification.
