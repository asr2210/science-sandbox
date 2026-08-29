# 003_motif_gradient

## What
50K sequences, stratified into 10 density bins (0..9 motifs per sequence). Motifs drawn from a 15-motif pool of strong K562/HepG2/SKNSH/universal activators (GATA1, KLF1, HNF4A, FOXA, CEBPA, MEF2, AP-1, SP1, NF-Y, USF, CREB, NF-kB).

## Why
Hypothesis: explicit motif content boosts variance both models agree on, raising r.

## Results
eval_01: 0.0959 (vs random 0.156) → **WORSE by 38%**
- K562_r: **0.073** (vs random 0.314) → CRASHED
- HepG2_r: 0.048 (vs 0.033) → tiny gain
- SKNSH_r: 0.167 (vs 0.121) → modest gain

eval_08: 0.555 (vs 0.579) → similar
eval_07/13: more negative (-0.21 vs -0.11) → confirms these are inversely related to motif density.

## Interpretation
- Motif insertion DISRUPTS the K562 axis. Pure random has natural k-mer statistics that both models agree on; injecting fixed motifs into some sequences but not others creates a non-natural k-mer mixture distribution that one model interprets but the other doesn't.
- The K562_r baseline of 0.31 from random must be driven by smooth k-mer / GC statistics — easy for both models to agree on. Discrete motifs break this.
- HepG2 and SKNSH responded mildly positively to motifs but not enough to overcome K562 collapse.

## Key insight
**Smooth, naturally-distributed variance > discrete motif insertions.** Don't disrupt the background statistics that the models naturally agree on.
