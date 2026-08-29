# 017 CpG=0.65 + TpA depletion (failed: polyA side effect)

50k 200bp Markov chain. Same CpG signal as 015 (T[C→G]=0.65) plus
T[T→A]=T[A→T]=0.10 (TpA AND ApT depleted ~55% vs iid).

Side effect: to maintain GC=0.55 with depleted A↔T transitions, T[A→A]
and T[T→T] rose to 0.50 (mean run length 2.0).

## Result
- mean_r = 0.819 (eval_01 = 0.836) — CATASTROPHIC, -0.049 vs 015
- K562 hit hardest: 0.83 → 0.75 on easy evals, 0.47 on eval_08
- HepG2 dropped 0.90 → 0.85
- SKNSH held at ~0.91 (slight drop from 0.92)

## Takeaway
**TpA depletion hurts catastrophically.** The polyA/polyT runs that came as
a side effect (T[A→A] = 0.50) likely confused the model. The model expected
random/uniform local structure and gets repeated A or T tracts.

Two lessons:
1. **Dinucleotide signals don't stack additively.** I cannot simply layer
   biology-motivated biases on top of CpG enrichment.
2. **Uniformity within sequences is critical.** Anything that creates
   visible local clustering (polyA, polyT) wrecks the model. This matches
   exp 011 (mixed-GC cross-sequence) failure. The model wants UNIFORM
   local distribution at all scales.

Even SKNSH (which was the big winner in 015) didn't gain here despite
keeping CpG=0.65, because the polyA disruption affected ALL cells.

## Next
- Drop TpA experiment direction
- Try 2nd-order Markov chain with trinucleotide enrichment (e.g., CGC,
  GCG) on top of 015's 1st-order CpG enrichment, without changing local
  uniformity
