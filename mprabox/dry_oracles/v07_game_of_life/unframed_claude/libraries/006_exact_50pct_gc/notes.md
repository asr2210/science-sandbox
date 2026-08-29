# 006_exact_50pct_gc

## Hypothesis
Removing the small natural per-seq GC noise from random uniform (binomial std ~3.5%) and forcing each sequence to be exactly 50% GC should give a small further boost beyond 0.398, *if* per-seq GC tightness is monotonically beneficial.

## Method
- For each seq, place exactly 100 GC bases at random positions, fill the rest with AT.
- Within GC positions, pick C or G uniformly. Within AT positions, pick A or T uniformly.
- N=50000, seed 42.

## Result
- **eval_01 mean_r = 0.3968** (K562=0.6177, HepG2=0.4365, SKNSH=0.1361)
- Essentially identical to random uniform (0.3981, diff -0.0013), within noise.

## Interpretation
Tightening GC variance from ~3.5% std down to 0% gives NO measurable improvement. The score function is flat in [~50% GC ± small noise]. The earlier penalty must kick in only at larger deviations.

So: random uniform is near a local plateau. Improving requires changing axes other than per-sequence GC.

## Next
- 007: high-complexity random (no homopolymer run > 3) — same GC, different dinuc structure.
- Later: motif-injected vs dinucleotide-controlled to probe other features.
