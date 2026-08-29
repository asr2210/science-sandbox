# Experiment 018 — CpG-stratified natural

## Design
10K natural windows per CpG-count bin: 0-1, 2-5, 6-12, 13-25, 26+.
Needed 8.5M genomic samples to fill the top bin (CpG ≥26 is rare).

## Result
- eval_01: 0.3923 (Δ +0.0047 vs nat baseline, -0.0016 vs GC-strat)
- K562: 0.6028, HepG2: 0.4285, SK-N-SH: 0.1458

CpG and GC are equivalent compositional levers, both reach ~0.392-0.394.

## Theory consolidation
**Any reasonable compositional balancing → 0.394 ceiling.**
The ceiling is intrinsic to model+eval given the v07 dynamic range
(0.025). Library design optimizations within composition space
have saturated.

## Where do I go from here?
Remaining open ideas, in order of plausibility:
1. **TSS-anchored library** (PLS only) — promoter-rich
2. **Synthesis best-of** — combine all positive levers into one library
3. **Mouse-heavy GC-strat** — test species after GC controlled
4. **Cell-type DHS components** — K562/HepG2/SK-N-SH targeted
5. **Sequence augmentation variants** — finer offsets, RC + offsets
6. **Hard negatives** — adjacent-to-cCRE windows

exp 019: TSS-anchored (PLS only).
