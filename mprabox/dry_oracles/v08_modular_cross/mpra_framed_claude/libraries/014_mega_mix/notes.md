# Experiment 014 — Mega-mix (motifs + pELS + dELS + PLS)

## What I tested
20k motifs + 10k pELS + 10k dELS + 10k PLS. Theory v3.6 predicted
each subset would still light up its eval.

## Result — mostly bad
- Mean across 14 ≈ -0.0003 (worst since exp 004).
- eval_13: K562=0.0161 (highest K562-on-13 ever, never lit before)
- eval_07: HepG2=0.0116, but mean only 0.0014 (K562 went -0.0014)
- eval_08: K562=0.0137 (high but unbalanced; was balanced at 012)
- eval_10: mean=0.0022 (dropped from dELS-only's 0.0085)
- HepG2 mostly NEGATIVE across most evals.

## What this tells me
**Dilution kills.** Cutting motif scaffolds from 35k to 20k destroyed
the broad baseline that was holding HepG2 positive. Each cCRE subset
at 10k is too small to deliver its full signal — got fragments of
each but lost the whole.

The 35k motif backbone was apparently doing more work than I gave
it credit for: it stabilized HepG2 across many evals.

## Updates to theory
**v3.6 → v3.7:** There's a critical mass threshold. 35k motif
scaffold seems to be near the floor for broad coverage. Below ~30k,
the model can't extract enough motif grammar to hold many evals.

cCRE classes at 15k each (as in 012/013) deliver near-full per-class
signal. At 10k each they only fire occasionally.

Therefore the optimal recipe is: keep motifs at 30-35k, share the
remaining 15-20k slots across at MOST 2 cCRE sub-classes.

## Next
Try **30k motifs + 10k pELS + 10k dELS** — keeps motif almost-full
and splits the remaining 20k between the two best enhancer classes.
If this hits both eval_08 and eval_10/13 simultaneously, mean will
climb. If not, we've found the dilution floor.
