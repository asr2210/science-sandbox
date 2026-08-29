# Experiment 017 — high-GC heavy library

## Design
60% windows from GC > 55% + 20% GC 45-55% + 20% GC < 45%.
All human natural.

## Result
- eval_01: 0.3928 (Δ -0.0011 vs uniform GC-strat 0.3939)
- K562: 0.6051, HepG2: 0.4291, SK-N-SH: 0.1442

Within noise but slightly below uniform GC. **Oversampling high-GC
doesn't help.**

## Interpretation
Eval doesn't want extra emphasis on high-GC. Uniform GC across bins
is roughly the optimal target distribution. Further GC tuning is not
a lever.

## Where the design space stands
The 0.394 ceiling is broadly reachable by **balancing the training
GC distribution to uniform across bins**. Deviating in either
direction (high-GC heavy here, low-GC heavy as nat baseline) drops.

## Next direction
Try a different compositional dimension: CpG dinucleotide content.
GC and CpG are correlated but not identical (CpG depleted in most
genome due to methylation). If CpG stratification helps orthogonally
to GC, both should be controlled.

exp 018: CpG-stratified natural sampling.
