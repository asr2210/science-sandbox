# 014 — Even stricter HepG2 (K25/H5/S20)

**Result:** mean_r = **0.0039** (tied with 013, new best). Per-cell:
- K562 avg = 0.0010 (DOWN from 013's 0.0020 — expanding K562 to 25k dilutes its quality)
- HepG2 avg = **0.0028** (UP from 013's 0.0021 — trend continues, marginal HepG2 is dilutive)
- SKNSH avg = 0.0078 (saturated)

K562 |lfc| threshold went 2.00 (20k) → 1.69 (25k); HepG2 |lfc| went 1.26 → 1.57.

**Theory update:** Every cell has a quality plateau. Beyond it, adding more sequences only adds noise.
- K562: optimum around 20k (|lfc|≥2.0)
- HepG2: keeps climbing as we shrink (best at 5k so far, |lfc|≥1.57)
- SKNSH: flat after ~16k

K562 lost 0.001 (per-cell r), HepG2 gained 0.0007 — net zero on mean. But the directionality is informative.

**Next (015):** Lock in optima — K562 20k (|lfc|≥2.0), HepG2 3-5k (even tighter), SKNSH gets the slack (~25-27k). Hoping for cleaner mean_r.
