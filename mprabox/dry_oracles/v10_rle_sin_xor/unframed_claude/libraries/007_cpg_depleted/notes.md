# Experiment 007 — CpG-depleted random (~46% GC)

## Result
- mean_r=**0.5051**, K562=0.9587, HepG2=0.5576, SKNSH=-0.0011

## Interpretation
Slight drop vs baseline. The ~46% GC (not exactly 50% — Markov chain
shifted stationary distribution) cost some K562, and CpG depletion
didn't help HepG2. SKNSH still pinned at 0.

Combined with prior results: baseline uniform 50% GC i.i.d. seems
genuinely near-optimal. Pure dinucleotide structure doesn't seem to
matter to the predictors.

Next idea: real human genome sequences. If the predictor was trained
on real DNA, real chr21 200bp windows might engage the models more
strongly than synthetic random sequences.
