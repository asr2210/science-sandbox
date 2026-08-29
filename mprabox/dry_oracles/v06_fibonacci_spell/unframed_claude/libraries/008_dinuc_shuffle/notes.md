# Experiment 008: Dinucleotide-shuffled genome windows

## Plan
Take exp 006 sequences and apply dinucleotide-preserving Eulerian shuffle
(verified to preserve all dinuc counts). If score ≈ raw, composition is
everything. If much lower, position/structure matters.

## Result
- eval_01 mean_r = **0.1326** (K562=0.038, HepG2=0.168, SKNSH=0.192)
- Drops 0.006 from raw genome (0.1387)
- Drops 0.020 from random (0.1176)

## Implication
~75% of the genome benefit is from k-mer/composition, ~25% from positional
structure. Both matter but composition dominates.

## eval_08 anomaly
Shuffled genome is the BEST library yet on eval_08 (0.0641). cCREs were
second-best on eval_08. eval_08 may reward composition-only signal and
penalize positional structure.

## Next
Test mix strategy (exp 009): combine high- and low-activity sources to
maximize variance. If variance drives r, this beats pure genome random.
