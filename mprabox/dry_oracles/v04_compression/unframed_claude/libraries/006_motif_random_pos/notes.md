# Experiment 006 — Random motifs at random positions

## What I tested
50K random uniform seqs, each with ONE motif chosen uniformly from 8 canonical TF binding sites (AP-1, SP1, NF-kB, GATA, CCAAT, TATA, E-box, HNF-like), inserted at a uniformly-random position.

## Result
eval_01: 0.331 → 0.328 (within noise — basically unchanged).
**eval_07: 0.420 → 0.447 (+0.027 — real improvement).**
**eval_13: 0.400 → 0.429 (+0.029 — real improvement).**
Most other evals near baseline; eval_10 slightly down (-0.011).

## Interpretation
HUGE theoretical insight: the AP-1 drop in exp 002 was due to FIXED POSITION (variance loss at columns 96-102), NOT the motif identity. When motifs are at varying positions AND varying identities, per-position nucleotide distribution stays uniform and the score is preserved.

Furthermore, some evals (07, 13) ACTIVELY REWARD motif content. Random uniform DNA was leaving signal on the table.

## Theory update → T4
- The scorer wants per-COLUMN nucleotide distribution to stay near uniform across the library (so it doesn't see structural bias at any single position).
- WITHIN-sequence motif content adds positive signal for some evals (notably eval_07 and eval_13) — these evals likely care about regulatory features.
- Other evals are insensitive to single motifs.
- The reward and cost are separable: motif=positive, fixed-position-structure=negative.

T4: Score-maximizing strategy = pack many motifs at varied positions, keeping per-column nucleotide distribution as uniform as possible.

## Next
Exp 007: Multiple motifs per sequence (e.g., 3-5 motifs at random positions, varied identities). Tests if more motif density per seq monotonically improves the motif-rewarding evals.
