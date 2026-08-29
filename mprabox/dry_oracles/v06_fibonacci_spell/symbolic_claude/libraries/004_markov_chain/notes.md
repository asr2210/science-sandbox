# 004 — Per-sequence Markov chain

## Setup
50K sequences. Each generated from its own 4x4 Markov chain whose rows
are Dirichlet(0.3). Sample initial state Dirichlet(0.3), then chain.

## Result
- eval_01 mean=0.1343 (k562=0.0380, hepg2=0.1684, sknsh=0.1967)
- ≈ Dirichlet-only (003: 0.1349). Marginal/flat.

## Interpretation
Dinucleotide structure beyond pure composition does NOT add r over
Dirichlet alone. So composition variance is the dominant accessible
gain so far. Further r increases probably require motif-level signals.
