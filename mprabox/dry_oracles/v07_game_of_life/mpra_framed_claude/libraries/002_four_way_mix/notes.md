# Experiment 002 — v04 best 4-way mix

## Design
20K natural human + 15K cCRE off-center + 10K DHS summit windows + 5K
mouse natural. Seed=0.

## Result
- eval_01: 0.394 (Δ +0.006 vs exp 001)
- K562: 0.604 (+0.008), HepG2: 0.430 (+0.007), SK-N-SH: 0.147 (+0.004)
- Per-eval gains: small and consistent (+0.005 to +0.007 on most evals)

## Interpretation
v04 lesson (4-way mix > natural alone) reproduces directionally in v07,
but the magnitude is smaller (+0.006 vs v04's +0.02). The mix helps
K562 most, SK-N-SH least. Regulatory-element enrichment is biased
toward the cell types where the regulatory elements were called from.
DHS Index is pan-tissue; cCREs are pan-tissue; both still favor the
"easy" cell types K562/HepG2.

## Implication
SK-N-SH gap is structural, not just a question of more regulatory
content. To boost SK-N-SH I need **neural-specific** regulatory content.
