# Experiment 005 — 41% GC i.i.d. (human-like composition)

## Result
- mean_r=**0.4742**, K562=0.8777, HepG2=0.5490, SKNSH=-0.0042

## Interpretation
GC curve (eval_01):
- 41% GC: K562=0.88
- 50% GC: K562=0.99
- 65% GC: K562=0.56

Sharp peak at 50%. K562 likes EXACTLY uniform 50%. HepG2 barely moves. SKNSH
still 0.

Confirms hypothesis: K562 r=0.99 is a low-variance artifact, not real
predictive signal. Drifting either way reduces it.
