# 014 — 10% uniform random dose (dose-response test)

**Hypothesis:** If 5% uniform (exp 013) was a free win, more might be
better. Test 10%.

**Design:** 20k genomic + 20k cCRE + 5k CpGi + 5k uniform random.

**Results vs exp 013 (best, mean=0.546):**
- eval_01:    0.5700 (-0.006)
- eval_04/09: 0.5705 (+0.001)
- eval_07:    0.5936 (-0.014) ← motif drop
- eval_08:    0.2284 (+0.026) ← OOD lift
- eval_13:    0.5719 (-0.014) ← motif drop
- eval_10:    0.5036 (-0.007)
- Mean:       **0.5413** (-0.004 vs 013)

**Findings:**

10% uniform random POLLUTES motif learning (eval_07/13 drop -0.014
each, eval_01 drops -0.006). The eval_08 lift (+0.026) doesn't
compensate. Dose-response peak is below 10%.

Order: exp 010 (0% uniform, mean=0.544) < exp 013 (5%, mean=0.546) >
exp 014 (10%, mean=0.541) >> exp 005 (33%, mean=0.500).

**Theory v6.3:** The sweet spot for uniform-random regularization is
~5%. Above that, the synthetic dilution starts eroding motif learning
faster than it lifts OOD. The curve is non-monotonic with peak at ~5%.

**Plan exp 015:** Stop sweeping the uniform dose; switch to testing
DIFFERENT OOD sources at the same 5% dose. Try mono-nucleotide
shuffled cCRE (cCRE base composition preserved, all motif structure
destroyed). This may be a better OOD source than uniform because it
matches genomic GC content while still being motif-free.

Composition: 22.5k genomic + 20k cCRE + 5k CpGi + 2.5k mono-shuffled
cCRE. Direct comparison to exp 013.
