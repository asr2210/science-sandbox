# Experiment 002 — 65% GC uniform i.i.d.

## What I did
50,000 i.i.d. 200bp sequences with P(G)=P(C)=0.325, P(A)=P(T)=0.175 (GC≈0.65).

## Result (eval_01)
- mean_r = **0.3551**  (was 0.5187 baseline, **−0.16**)
- k562_r = 0.5642 (was 0.9947, **−0.43**)
- hepg2_r = 0.5121 (was 0.5669, −0.05)
- sknsh_r = -0.0111 (was -0.0054, ~same)

## Interpretation
**GC-biased sequences are MUCH worse for K562.** Random uniform 50% GC seems
to be a sweet spot for the K562 predictor — or possibly the K562 r=0.99 with
random was artificially high (low variance in predictions inflating correlation).
SKNSH still at zero; HepG2 barely moved.

K562 is sensitive to base composition; HepG2 weakly so; SKNSH appears
indifferent to nucleotide frequencies alone.

eval_08 again behaves differently: K562 still 0.86 (vs 0.56 typical), HepG2
drops to 0.38. Maybe eval_08 uses a different K562 model that *prefers* GC-rich?

## Next
Don't bias overall composition. Instead try injecting strong known TF motifs
into otherwise-random sequences. If the per-cell-type models agree on what
motifs do, lifting SKNSH r above 0 should be possible.
