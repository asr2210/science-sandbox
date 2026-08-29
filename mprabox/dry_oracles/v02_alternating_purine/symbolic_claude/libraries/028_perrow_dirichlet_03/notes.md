# Exp 028 — per-row Dirichlet(0.3) noise direction

## Result
eval_01 = 0.1630 (vs 0.1628 Dirichlet(1)). Essentially tied.
condition_c = 0.4246. Same lift.

## Interpretation
Alpha parameter (per-row noise concentration) doesn't matter much.
Any per-row noise variation suffices. Could be the BINARY presence
of per-row variation is what matters, not its magnitude.

## Next
Try Dirichlet over ALL 4 directions (per-row p AND noise variation).
This adds per-row p variance ON TOP of per-row noise direction.
Use α=(2.1, 0.3, 0.3, 0.3) for mean p=0.7 with std~0.23.
If continued lift → per-row p variation also helps.
