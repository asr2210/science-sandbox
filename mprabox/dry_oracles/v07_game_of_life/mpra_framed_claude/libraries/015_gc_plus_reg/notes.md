# Experiment 015 — GC-stratified + regulatory mix combination

## Design
25K GC-stratified natural (5K/bin) + 15K GC-stratified cCRE
(3K/bin) + 10K GC-stratified DHS (2K/bin). Each source separately
balanced across the 5 GC bins.

## Result
- eval_01: 0.3945
- vs GC-strat alone (014): 0.3939 (+0.0006)
- vs 4-way mix (002): 0.3937 (+0.0008)
- All within noise floor (~0.002)

## T8 fully confirmed
GC stratification and regulatory enrichment are the **same
mechanism**. Combining them gives no additional lift beyond
either alone. The ceiling is set by GC distribution coverage.

## Where we stand at exp 015
| design | eval_01 |
|---|---|
| 4-way mix (s=1) | 0.3961 |
| GC + reg combo | 0.3945 |
| GC-stratified | 0.3939 |
| max diversity | 0.3939 |
| 4-way mix (s=0) | 0.3937 |
| activity contrast | 0.3934 |
| natural | 0.3876 |

The ceiling is **0.394 ± 0.002** with library design alone. We've
hit it via 3 independent routes. Library design has nothing more
to give on the "what to include in the natural distribution" axis.

## Next direction
True orthogonality search. Untested dimensions:
- **Shifted-window augmentation** (positional invariance training)
- **Synthetic motif planting** (model learns motif → activity links)
- **Mouse-heavy** (>50% mouse — push species generalization)
- **Anti-repeat sampling** (mask out repetitive elements)

exp 016: shifted-window augmentation. 10K anchor sites, each
yielding 5 windows at offsets -50,-25,0,+25,+50. Tests whether
model trained with positional-invariance signal generalizes
better.
