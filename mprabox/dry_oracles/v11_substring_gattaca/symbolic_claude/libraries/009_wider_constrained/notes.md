# 009 wider_constrained [43,57] — BIG jump!

Range [43,57]. Uniform over valid count tuples (2255 tuples). Shuffle within seq.

Result: eval_01 mean_r = **0.8820** (+0.022 over 007's 0.8597, +0.029 over uniform random).

Conditions:
- a: 0.856 (similar to 007's 0.865)
- b: 0.909 (vs 0.919 in 007) — slight drop
- c: **0.881** (vs 0.796 in 007, 0.834 in uniform) — big jump!

Key insight: the gain isn't simply tight composition. It's **uniform-over-tuples**
sampling that creates a flat distribution over many distinct compositions.
This boosts inter-sequence compositional diversity in a controlled way.

Compositional std isn't the right summary — distribution shape matters.
i.i.d. multinomial concentrates near (50,50,50,50); uniform-over-tuples spreads out.

Direction: try [40,60], [38,62] to see if even broader uniform sampling helps.
