# 015 multinomial_truncated [43,57]

Same range as 009 but i.i.d. multinomial sampling (rejected if outside [43,57]),
NOT uniform-over-tuples. The marginal composition distribution is bell-shaped
(concentrated near 50,50,50,50) instead of flat.

Result: eval_01 mean_r = **0.8767** (slightly worse than 009's 0.8820).

Conditions vs 009:
- a: 0.857 (≈ same)
- b: 0.915 (slightly UP from 0.909)
- c: 0.858 (DOWN from 0.881)

CONFIRMED: the SHAPE of the composition distribution matters. Uniform-over-tuples
(flat) gives slightly higher c at slight cost to b. Net win.

Further direction: try Markov chain with [43,57] rejection — tests if within-string
structure (autocorrelation, dinucleotide) helps when composition is right.
