# 025 — Triple bank (K562 + SKNSH + HepG2 each engineered)

## Method
3 banks of ~16.7k each, internal 50/50 active/null:
- K562: exp 012 design (GC=65 12 motifs vs GC=25)
- SKNSH: exp 024 design (K562 motifs GC=60 vs GC=40)
- HepG2: real H3K27ac peaks + dinuc-shuffled

## Results (eval_01)
mean_r = -0.0016 (K562=-0.0016, HepG2=-0.0087, SKNSH=+0.0055)

## Lesson
- Triple-bank FAILED. Worse than any single-cell focused design.
- K562 r dropped from +0.0089 (exp 012, 50k bank) to -0.0016 (16.7k bank).
  Not just diluted — flipped sign. Other banks confounded K562 predictor.
- HepG2 went deeply negative (-0.0087). The K562 + SKNSH banks' GC=25/40
  null halves cluster low-GC, which HepG2 might rank as "HepG2-like
  positive" — opposite of intended.
- eval_07 = +0.0054 (HepG2=+0.0145), eval_08 = +0.0048.

## Implication
- Cross-bank pollution destroys per-cell r more than additive lift gains.
- Single-cell focused designs (50k dedicated to one cell) win.
- Plateau at +0.0045 (exp 012) is real — hard to beat by composition.

## Next (exp 026)
Try HYBRID GENOMIC: take real K562 H3K27ac peaks (natural enhancer context)
and ADD inserted K562 motifs to densify them. Natural backbone might
provide what the model needs; added motifs amplify.
