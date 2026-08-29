# Experiment 020 — GC-stratified human + GC-stratified mouse

## Design
25K hg38 GC-stratified (5K/bin) + 25K mm39 GC-stratified (5K/bin).

## Result
- eval_01: 0.3947 (Δ +0.0008 vs GC-strat human alone)
- K562: 0.6070, HepG2: 0.4308, SK-N-SH: 0.1463

Within noise. **Multi-genome under composition control does not
beat single-genome.**

## Interpretation
Confirms T4 (species-agnostic): once GC is balanced, mouse provides
no additional information beyond human. The model has internalized
sequence-level generalization that crosses species. Library design
across genomes is fungible at the ceiling.

## Ceiling cluster (updated)
| design | eval_01 |
|---|---|
| 4-way mix s=1 (010) | 0.3961 |
| **multi-genome GC (020)** | **0.3947** |
| GC + reg (015) | 0.3945 |
| GC-strat human (014) | 0.3939 |
| max diversity (009) | 0.3939 |
| 4-way mix s=0 (002) | 0.3937 |

All within ±0.002 of 0.394. The ceiling is rock solid.

## Next direction
Cell-type diversity in DHS — sample DHS summits across diverse
components evenly. Tests whether broader cell-type coverage
(beyond the 3 labeled K562/HepG2/SK-N-SH) helps unseen-cell-type
generalization.
