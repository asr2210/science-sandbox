# 018_multi_source

## Design
1,000 regions x 10 tiles from each of 5 orthogonal sources:
broad cCRE, K562 DHS, HepG2 DHS, SKNSH DHS, conservation-top cCRE.
50K total, 5K total regions = saturating.

## Result vs 014 (5K x 10 broad cCRE)
                eval_01  K562    HepG2   SKNSH
014 5K x 10:    0.3181   0.144   0.188   0.623
018 multi-src:  0.3121   0.135   0.176   0.625

DOWN by 0.006. K562 and HepG2 take small hits.

## Interpretation
Multi-source mixing slightly HURTS — likely because the conserved
cCRE component carries the same variance-narrowing penalty seen in
016 (-0.012 from same allocation). Mixing it with broader sources
dilutes but doesn't eliminate its drag.

## NEW finding: K562 head is library-INSENSITIVE
Cross-checked K562 scores across libraries:
- 001 random:        K562=0.140
- 002 cCRE:          K562=0.145
- 005 cCRE dense:    K562=0.146
- 006 synth:         K562=0.140
- 010 differential:  K562=0.139
- 012 RC aug:        K562=0.144
- 014 5K x 10:       K562=0.144
- 017 class-bal:     K562=0.141
- 018 multi-src:     K562=0.135

K562 is pinned at 0.139-0.146 across EVERY library tested,
including random and synthetic. **The K562 head's predictive
capacity for eval_01 K562 is architecture-bound, not library-
bound** — there's no library design that lifts K562 above ~0.146
in this experimental envelope.

SKNSH similarly bounded at ~0.60-0.66 (more variable but still
narrow).

HepG2 is the only LIBRARY-SENSITIVE head:
- random/synth: HepG2 = -0.07 to -0.09 (anti-predicted!)
- cCRE-based:   HepG2 = 0.18 to 0.19
- HepG2 peak:   0.191 (012 RC)

## Theory T11 → T12 (new!)
mean_r = (K562 + HepG2 + SKNSH) / 3 = (~0.14 + HepG2 + ~0.625) / 3
       ≈ (0.765 + HepG2) / 3
       ≈ 0.255 + HepG2/3

To lift mean_r above 0.32 → need HepG2 > 0.195.
To lift mean_r above 0.33 → need HepG2 > 0.225.

The K562 head is essentially MAXED OUT at 0.146 regardless of
library content. SKNSH max around 0.64. **Mean_r is bottlenecked
by HepG2 prediction**, which is the only library-variable head.

The "plateau" is therefore not just an architectural ceiling — it
is the HepG2-head ceiling under all natural-genomic libraries
tested (max ~0.191).

## Next
Experiment 019: HepG2-OPTIMIZED library. 5,000 HepG2-specific DHS
peaks (HepG2 DHS NOT in K562 NOT in SKNSH, top by signal) × 10
tiles = 50K. Maximizes HepG2-specific regulatory exposure to
push the HepG2 head toward its ceiling.

Generalization justification: even though this maximally biases
toward HepG2-specific content, the regulatory grammar learned is
universal — TF binding rules, motif spacing, contextual modulators
— and applies to any cell type's HepG2-style regulatory regions.
If the HepG2 head ceiling is hit, mean_r lifts. Trade-off: K562
and SKNSH may drop slightly since less per-cell-type-specific
content for them.
