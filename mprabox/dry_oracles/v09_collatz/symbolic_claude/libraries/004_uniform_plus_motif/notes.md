# 004 — Uniform random + 12bp motif at random position

Each sequence is iid uniform, with a 12-character motif
"012301230123" overwriting a random window.

## Result
- eval_01: mean_r=0.2235 (vs 0.2399 baseline) — DOWN
- a: 0.139 (≈ same), b: -0.087 (worse), c: 0.618 (slightly down)

## Interpretation
Adding a randomly-placed structured motif slightly HURT b — the
opposite of prediction. b doesn't reward arbitrary structure.
Hypothesis: b rewards CROSS-sequence alignment / shared positions,
which random-position insertion doesn't provide.

Next: place a scaffold at FIXED position across all sequences so
they share content at the same coordinates, then see whether b reacts.
