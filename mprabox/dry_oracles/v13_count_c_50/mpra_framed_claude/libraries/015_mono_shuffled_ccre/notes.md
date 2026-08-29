# 015 — 5% mono-shuffled cCRE as OOD source

**Hypothesis:** Mono-nucleotide shuffled cCRE preserves base composition
(matches genomic GC) while destroying all motifs. Should be a softer
OOD signal than uniform random — eval_08 lift without motif cost.

**Design:** 22.5k genomic + 20k cCRE + 5k CpGi + 2.5k mono-shuffled
cCRE. Direct comparison to exp 013 (uniform random instead of shuffled).

**Results vs exp 013 (5% uniform random, mean=0.546):**
- eval_01:    0.5761 (+0.0003) ~ tied
- eval_04/09: 0.5687 (-0.001)
- eval_07:    0.6105 (+0.003) ← slight motif lift
- eval_08:    0.1943 (-0.008) ← OOD slightly less
- eval_13:    0.5895 (+0.003) ← slight motif lift
- eval_10:    0.5110 (+0.001)
- Mean:       **0.5456** (+0.0001 — tied with NEW BEST)

**Findings:**

Mono-shuffled cCRE gives EQUAL mean to uniform random, but with a
different tradeoff:
- Uniform random: stronger eval_08 lift, slight motif drop
- Mono-shuffled: weaker eval_08 lift, slight motif gain

Both are valid "synthetic regularization" sources. The composition-
matching of mono-shuffled gives less OOD signal but preserves motif
learning better.

**Theory v6.4:** Synthetic regularization works through TWO mechanisms:
1. **Composition extremity** (uniform random) — exposes model to base
   distributions it wouldn't otherwise see; helps OOD
2. **Order destruction** (mono-shuffled) — keeps composition, breaks
   motif structure; helps model learn "presence of motif" vs random arrangement

Either single mechanism at 5% gives ~+0.002 over no synthetic. May be
worth COMBINING them at smaller doses each.

**Plan exp 016:** Try combining uniform + mono-shuffled at 2.5% each
(total 5% synthetic, split). If complementary, may exceed either alone.
Composition: 22.5k genomic + 20k cCRE + 5k CpGi + 1.25k uniform +
1.25k mono-shuffled.
