# Exp 013: forced 50:50:50:50 per sequence

**Hypothesis**: Per-seq GC variance hurt K562/HepG2 in mono-shuffled
natural (Exp 012). Forcing exact balance per sequence should boost.

**Method**: Every 200bp seq = shuffled (50A + 50C + 50G + 50T).

**Results**: eval_01=0.3242, K562=0.4448, HepG2=0.4910, SKNSH=0.0368.
ALL metrics dropped sharply — this is even worse than the biased
composition libraries (Exp 003, 004).

**Interpretation**: Per-seq composition variance is GOOD, not bad.
Random has Binomial(200, 0.5) variance ≈ 50% ± 3.5%. Forcing ZERO
variance crushes the model's predictions — it expects natural-ish
per-sequence variation. So:
- Too much variance (natural 30-70%): hurts K562/HepG2
- Random's natural binomial variance: optimal
- Zero variance (Exp 013): hurts everything

There's a sweet spot exactly at random.

**Implication**: Don't try to constrain composition tighter. The optimum
along this axis is already at random.
